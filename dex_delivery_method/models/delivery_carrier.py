
import logging

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools.safe_eval import safe_eval

_logger = logging.getLogger(__name__)

class DeliveryCarrier_Inh(models.Model):
    _inherit = 'delivery.carrier'
   
    
    delivery_type = fields.Selection([('fixed', 'Fixed Price'), 
                                      ('base_on_rule', 'Based on Rules'),
                                      ('base_on_percent', 'Based on Percentage')],
                                      string='Provider', default='fixed', required=True)
    percent= fields.Float("Percentage")
    price_rule_ids = fields.One2many('delivery.price.rule', 'carrier_id', 'Pricing Rules', copy=True)
    based_on = fields.Selection([('ordered_qty','Ordered Quantity'),
                                 ('deliverd_qty','Delivered Quantity')],string="Based On",default='deliverd_qty')
    
    
    @api.multi
    def get_price_available_custom_ordered_qty(self, order):
        print"get_price_available_custom_ordered_qty"
        self.ensure_one()
        total = weight = volume = quantity = 0
        total_delivery = 0.0
        for line in order.order_line:
            if line.add_charge_applicable == True:
                
                if line.state == 'cancel':
                    continue
                if 'add_charges_ids' in order._fields:
                    if line.is_delivery:
                        total_delivery += line.price_total
                    if not line.product_id or line.is_delivery:
                        continue
                    qty = line.product_uom._compute_quantity(line.product_uom_qty, line.product_id.uom_id)
                    
                
                else:
                    total_delivery += line.price_total
                    qty = line.product_uom._compute_quantity(line.product_qty , line.product_id.uom_id)
                
                weight += (line.product_id.weight or 0.0) * qty
                volume += (line.product_id.volume or 0.0) * qty
                quantity += qty
        print("quantity: ",quantity,"--volume:",volume,"--weight:",weight)
        total = (order.amount_total or 0.0) - total_delivery

        total = order.currency_id.with_context(date=order.date_order).compute(total, order.company_id.currency_id)

        return self.get_price_from_picking_custom(total, weight, volume, quantity)
    
    
    @api.multi
    def get_price_available_custom_delivered_qty(self, order):
        print"get_price_available_custom_delivered_qty"
        self.ensure_one()
        total = weight = volume = quantity = 0
        total_delivery = 0.0
        for line in order.order_line:
            if line.add_charge_applicable == True:
                
                if line.state == 'cancel':
                    continue
                if 'add_charges_ids' in order._fields:
                    if line.is_delivery:
                        total_delivery += line.price_total
                    if not line.product_id or line.is_delivery:
                        continue
                    qty = line.qty_delivered
                    
                
                else:
                    total_delivery += line.price_total
                    qty = line.qty_received
                
                weight += (line.product_id.weight or 0.0) * qty
                volume += (line.product_id.volume or 0.0) * qty
                quantity += qty
        print("quantity: ",quantity,"--volume:",volume,"--weight:",weight)
        total = (order.amount_total or 0.0) - total_delivery

        total = order.currency_id.with_context(date=order.date_order).compute(total, order.company_id.currency_id)

        return self.get_price_from_picking_custom(total, weight, volume, quantity)
    
    def get_price_from_picking_custom(self, total, weight, volume, quantity):
        price = 0.0
        criteria_found = False
        price_dict = {'price': total, 'volume': volume, 'weight': weight, 'wv': volume * weight, 'quantity': quantity}
        for line in self.price_rule_ids:
            test = safe_eval(line.variable + line.operator + str(line.max_value), price_dict)
            print("-------------test",test,"xpr:---",line.variable + line.operator + str(line.max_value))
            if test:
                price = line.list_base_price + line.list_price * price_dict[line.variable_factor]
                criteria_found = True
                break
#         if not criteria_found:
#             raise UserError(_("Selected product in the delivery method doesn't fulfill any of the delivery carrier(s) criteria."))

        return price
    
    
    @api.one
    def get_price(self):
        SaleOrder = self.env['sale.order']

        self.available = False
        self.price = False

        order_id = self.env.context.get('order_id')
        if order_id:
            # FIXME: temporary hack until we refactor the delivery API in master

            order = SaleOrder.browse(order_id)
            if self.delivery_type not in ['fixed', 'base_on_rule','base_on_percent']:
                try:
                    computed_price = self.get_shipping_price_from_so(order)[0]
                    self.available = True
                except ValidationError as e:
                    # No suitable delivery method found, probably configuration error
                    _logger.info("Carrier %s: %s, not found", self.name, e.name)
                    computed_price = 0.0
            else:
                carrier = self.verify_carrier(order.partner_shipping_id)
                if carrier:
                    try:
                        computed_price = carrier.get_price_available(order)
                        self.available = True
                    except UserError as e:
                        # No suitable delivery method found, probably configuration error
                        _logger.info("Carrier %s: %s", carrier.name, e.name)
                        computed_price = 0.0
                else:
                    computed_price = 0.0

            self.price = computed_price * (1.0 + (float(self.margin) / 100.0))
   
    @api.multi
    def create_price_rules(self):
        PriceRule = self.env['delivery.price.rule']
        for record in self:
            # If using advanced pricing per destination: do not change
            if record.delivery_type == 'base_on_rule':
                continue

            # Not using advanced pricing per destination: override lines
            if record.delivery_type == 'base_on_rule' and not (record.fixed_price is not False or record.free_if_more_than):
                record.price_rule_ids.unlink()

            # Check that float, else 0.0 is False
            if not (record.fixed_price is not False or record.free_if_more_than):
                continue
            
            if not (record.percent is not False):
                continue
            
            if record.delivery_type == 'base_on_percent':
                PriceRule.search([('carrier_id', '=', record.id)]).unlink()
                line_data = {
                    'carrier_id': record.id,
                    'variable': 'price',
                    'operator': '>=',
                }
                
                if record.percent is not False:
                    line_data.update({
                        'max_value': 0.0,
                        'standard_price': record.percent,
                        'list_base_price': record.percent,
                    })
                    PriceRule.create(line_data)
            
            if record.delivery_type == 'fixed':
                PriceRule.search([('carrier_id', '=', record.id)]).unlink()

                line_data = {
                    'carrier_id': record.id,
                    'variable': 'price',
                    'operator': '>=',
                }
                # Create the delivery price rules
                if record.free_if_more_than:
                    line_data.update({
                        'max_value': record.amount,
                        'standard_price': 0.0,
                        'list_base_price': 0.0,
                    })
                    PriceRule.create(line_data)
                if record.fixed_price is not False:
                    line_data.update({
                        'max_value': 0.0,
                        'standard_price': record.fixed_price,
                        'list_base_price': record.fixed_price,
                    })
                    PriceRule.create(line_data)
        return True
 
 
