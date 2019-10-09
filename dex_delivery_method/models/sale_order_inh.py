
from odoo import api, fields, models,_
from odoo.exceptions import UserError, ValidationError


class SaleOrderLineInherit(models.Model):
    _inherit = "sale.order.line"
     
    add_charge_applicable = fields.Boolean(string="Additional Charge Applicable",default=True)

    

class SaleOrder(models.Model):
    _inherit = "sale.order"
    
    add_charges_ids = fields.One2many('additional.charges','additonal_id', string="Additional Charges",copy=True)
    
    sol_additional_chrg_line_ids = fields.One2many('sol.additional.charges','so_additional_chrg_id',string="SOL Additional charges IDs")
    
    
    @api.multi
#     def action_invoice_create(self, grouped=False, final=False):
#           
#         res = super(SaleOrder,self).action_invoice_create(grouped,final)
#         print"======res",res
# #         print"=======invoice_count",self.invoice_count
# #         print"==invoice_ids",self.invoice_ids
#         
#         for invoice_id in res:
#             invoice = self.env['account.invoice'].browse(invoice_id)
#             if self.sol_additional_chrg_line_ids:
#                 if len(self.invoice_ids) ==1:
#                     for add_charge_id in self.sol_additional_chrg_line_ids:
#                         account = add_charge_id.product_id.property_account_income_id or add_charge_id.product_id.categ_id.property_account_income_categ_id
#                         if not account:
#                             raise UserError(_('Please define income account for this product: "%s" (id:%d) - or for its category: "%s".') %
#                                 (add_charge_id.product_id.name, add_charge_id.product_id.id, add_charge_id.product_id.categ_id.name))
#                   
#                         fpos = add_charge_id.so_additional_chrg_id.fiscal_position_id or add_charge_id.so_additional_chrg_id.partner_id.property_account_position_id
#                         if fpos:
#                             account = fpos.map_account(account)
#                               
#                             ail = {
#                                     'name': add_charge_id.name,
#                                     'sequence': invoice.invoice_line_ids[-1].sequence + 1,
#                                     'account_id': account.id,
#                                     'price_unit': add_charge_id.price_unit,
#                                     'quantity': add_charge_id.qty_delivered,
#                                     'discount': add_charge_id.discount,
#                                     'uom_id': add_charge_id.product_uom.id,
#                                     'product_id': add_charge_id.product_id.id or False,
#                                     'invoice_line_tax_ids': [(6, 0, add_charge_id.product_id.taxes_id.ids)],
#                                     'invoice_id': invoice_id
#                                     }
#               
#                             print"===ail",ail
#                             if ail['price_unit']>0:
#                                 id = self.env['account.invoice.line'].create(ail)
#                                 
# #                                 invoice._onchange_invoice_line_ids()
# #                                 id._onchange_product_id()
# #                                 id.price_unit= add_charge_id.price_unit
# #                                 id._compute_price()
# #                                 print"id--",id
# #                                 taxes= []
# #                                 print("===========taxes",invoice.tax_line_ids)
# #                                 taxes = invoice.tax_line_ids.ids
# #                                 taxes.extend(add_charge_id.product_id.taxes_id.ids)
# #                                 print("========taxes",taxes)
# #                                 invoice.tax_line_ids = [(6, 0,taxes)]
#                         invoice._compute_amount()
# #                             id = self.env['account.invoice.line'].create(ail)
#                                 
#                 
#                 else:
#                     
#                     for add_charge_id in self.sol_additional_chrg_line_ids:
#                         
#                         old_invoice = self.env['account.invoice'].search([('id','in',self.invoice_ids.ids)],order='date_invoice desc')
# #                         print"old_invoice",old_invoice
# #                         print"old_invoice",old_invoice[1]
#                                     
#                                     
#                         for inv_line in old_invoice[1].invoice_line_ids:
#                             if inv_line.product_id == add_charge_id.product_id:
#                                 if inv_line.price_unit <= add_charge_id.price_unit:
#                         
#                                     account = add_charge_id.product_id.property_account_income_id or add_charge_id.product_id.categ_id.property_account_income_categ_id
#                                     if not account:
#                                         raise UserError(_('Please define income account for this product: "%s" (id:%d) - or for its category: "%s".') %
#                                             (add_charge_id.product_id.name, add_charge_id.product_id.id, add_charge_id.product_id.categ_id.name))
#                               
#                                     fpos = add_charge_id.so_additional_chrg_id.fiscal_position_id or add_charge_id.so_additional_chrg_id.partner_id.property_account_position_id
#                                     if fpos:
#                                         account = fpos.map_account(account)
#                                           
#                                         ail = {
#                                                 'name': add_charge_id.name,
#                                                 'sequence': invoice.invoice_line_ids[-1].sequence + 1,
#                                                 'account_id': account.id,
#                                                 'price_unit': (add_charge_id.price_unit - inv_line.price_unit),
#                                                 'quantity': add_charge_id.qty_delivered,
#                                                 'discount': add_charge_id.discount,
#                                                 'uom_id': add_charge_id.product_uom.id,
#                                                 'product_id': add_charge_id.product_id.id or False,
#                                                 'invoice_line_tax_ids': [(6, 0, add_charge_id.product_id.taxes_id.ids)],
#                                                 'invoice_id': invoice_id
#                                                 }
#                           
# #                                         print"===ail",ail
#                                         if ail['price_unit']>0:
#                                             id = self.env['account.invoice.line'].create(ail)
#                                             print("===========taxes",invoice.tax_line_ids)
#                                             invoice._compute_amount()
#         return res                          
    
#     @api.model
#     def create(self, vals):
#         print"******* save button code***************"
#         result = super(SaleOrder, self).create(vals)
# #         result.compute_method()
#         result.save_button()
#         return result
     
    @api.multi
    def delivery_set_limit(self):
        for order in self:
            for line in order.add_charges_ids:
#                 for c_id in line.carrier_id:
                    carrier = line.carrier_id
                    if line:
                        if order.state not in ('draft', 'sent','sale','done'):
                            raise UserError(_('The order state have to be draft to add delivery lines.'))
        
                        if carrier.delivery_type not in ['fixed','base_on_rule','base_on_percent']:
#                             print '^^^^^^^^^^^^^^^^^^^^^^1 first'
                            # Shipping providers are used when delivery_type is other than 'fixed' or 'base_on_rule'
                            price_unit = order.carrier_id.get_shipping_price_from_so(order)[0]
#                             print "_________1st ____________",price_unit

                        else:
                            # Classic grid-based carriers
                            carrier = line.carrier_id.verify_carrier(order.partner_shipping_id)
                            print "----------- carrier line -----------------",carrier
                            if not carrier:
                                raise UserError(_('No carrier matching.'))
                            
                            price_unit = carrier.get_price_available(order)
                            print  "_______________2nd___________",price_unit
                           
                            if order.company_id.currency_id.id != order.pricelist_id.currency_id.id:
                                price_unit = order.company_id.currency_id.with_context(date=order.date_order).compute(price_unit, order.pricelist_id.currency_id)
                                print"__________3rd________",price_unit
                        
                        final_price = price_unit * (1.0 + (float(self.carrier_id.margin) / 100.0))
                        print"____________________________",final_price
                        
#                         for o_line in order.order_line:
#                             print "RRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR",line.carrier_id.product_id,o_line.product_id
#                             if line.carrier_id.product_id == o_line.product_id:
#                                 self.delivery_unset(o_line)
                        
#                         -------------------------------------

                        print"order===",order
                        if line.carrier_id.delivery_type == 'fixed':
                            ordered_qty = delivered_qty = 0
                            if line.additonal_id:
                                for o in line.additonal_id.order_line:
                                    if o.add_charge_applicable == True:
                                        ordered_qty += o.product_uom_qty
                                        if line.carrier_id.based_on == 'deliverd_qty':
                                            if o.qty_delivered > 0.0:
                                                delivered_qty += o.qty_delivered
                                        else:
                                            delivered_qty += o.product_uom_qty        
                            delivered_total=(line.delivery_price/ordered_qty)*delivered_qty
                        
                        if line.carrier_id.delivery_type == 'base_on_rule':
                            if line.carrier_id.based_on == 'ordered_qty':
                                delivered_total = line.carrier_id.get_price_available_custom_ordered_qty(line.additonal_id)
                            else:
                                delivered_total = line.carrier_id.get_price_available_custom_delivered_qty(line.additonal_id)
                                
                        if line.carrier_id.delivery_type == 'base_on_percent':
                            amt = 0.0
                            l=line.percent
                            if line.additonal_id:
                                for o in line.additonal_id.order_line:
                                    if o.add_charge_applicable == True:
                                        if line.carrier_id.based_on == 'deliverd_qty':
                                            if o.qty_delivered > 0.0:
                                                amt += (o.price_unit * o.qty_delivered)
                                        else:        
                                            amt += (o.price_unit * o.product_uom_qty)
                            
                            f_amount = amt*(l/100)
                            print "+++++++++++++ final amount",f_amount
                            delivered_total=f_amount

                        order._create_delivery_line(carrier, final_price,line,delivered_total)
                       
                    else:
                        raise UserError(_('No carrier set for this order.'))

        return True
    
#   Method to delete existing record from sale order line,while set record of delivery charges 
    @api.multi
    def delivery_unset(self,o_line):
        o_line.unlink()
    
    
    
#   Method to set record in sale order line
    def _create_delivery_line(self, carrier, price_unit,line,delivered_total):
#         print"___ enter sale order creation____________"
        print"====",carrier,"===",line
        
        
        SaleOrderLine = self.env['sol.additional.charges']
        # Apply fiscal position
        taxes = carrier.product_id.taxes_id.filtered(lambda t: t.company_id.id == self.company_id.id)
        print"taxes==",taxes
        taxes_ids = taxes.ids
        if self.partner_id and self.fiscal_position_id:
            taxes_ids = self.fiscal_position_id.map_tax(taxes, carrier.product_id, self.partner_id).ids
        # Create the sale order line
        print"111taxes",taxes_ids
        values = {
#             'order_id': self.id,
            'so_additional_chrg_id':self.id,
            'name': carrier.name,
            'product_uom_qty': 1,
            'product_uom': carrier.product_id.uom_id.id,
            'product_id': carrier.product_id.id,
            'price_unit':delivered_total,
#             'tax_id': [(6, 0, taxes_ids)],
            'is_delivery': True,
            'qty_delivered':1,
#             'delivered_total':delivered_total,
            'add_charge_applicable':False,
            
        }
        if self.sol_additional_chrg_line_ids:
            values['sequence'] = self.sol_additional_chrg_line_ids[-1].sequence + 1
        
        print"======self.sol_additional_chrg_line_ids",self.sol_additional_chrg_line_ids    
        check = False
        for o_line in self.sol_additional_chrg_line_ids:
            print "RRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR",line.carrier_id.product_id,o_line.product_id
            if o_line.product_id == line.carrier_id.product_id:
#                 print"1"
                o_line.price_unit =  delivered_total
                return o_line
            else:   
#                 print"2"
                check = True
                
        if check == True or not self.sol_additional_chrg_line_ids:
#             print"3"
            sol = SaleOrderLine.create(values)
        return sol
    
    @api.multi
    def save_button(self):
        print"******* compute method********"
        for order in self:
            for c_id in order.add_charges_ids:
                if c_id.carrier_id.delivery_type == 'base_on_rule':
                    c_id.delivery_price = c_id.carrier_id.with_context(order_id=order.id).price
                    print "===============",c_id.delivery_price

    @api.multi
    def compute_method(self):
        for order in self:
            order.compute_delivery_price()
    @api.multi
    def compute_delivery_price(self):
        print"***********compute_delivery_price***********"
        for order in self:
            for c_id in order.add_charges_ids:
                if order.state != 'draft':
                    continue
                if c_id.carrier_id.delivery_type == 'fixed' or c_id.carrier_id.delivery_type == 'base_on_rule':
                    c_id.delivery_price = c_id.carrier_id.with_context(order_id=order.id).price
                    print"_______rule base____________",c_id.delivery_price       
                
                if c_id.carrier_id.delivery_type == 'base_on_percent':
                    print ""      
                    c_id.percent=c_id.carrier_id.percent
                    print"_______percent base____________",c_id.percent



            
class SOL_Additional_charges(models.Model):
    _name  = "sol.additional.charges"
    
    sequence = fields.Integer(string='Sequence')
    
    so_additional_chrg_id = fields.Many2one('sale.order',string="So Additional charges ID")
    
    name = fields.Char(string='Name')
    product_uom_qty = fields.Float('Product Qty')
    product_id = fields.Many2one('product.product',string="Product ID")
    price_unit = fields.Float(string='Unit Price')
    tax_id = fields.Many2many('account.tax',string='Taxes')
    
    qty_delivered = fields.Float(string='Quantity Delivered')
    add_charge_applicable = fields.Boolean(string='Additional Charges applicable')
    
    product_uom = fields.Many2one('product.uom',string='Product UOM')
    is_delivery = fields.Boolean(string='Delivery')
    discount = fields.Float(string='Discount')
    
    cgst = fields.Float(string='CGST', compute='_compute_gst', store=True)
    sgst = fields.Float(string='SGST', compute='_compute_gst')
    igst = fields.Float(string='IGST', compute='_compute_gst')
    amount = fields.Float(string='Amt. with Taxes', readonly=True, compute='_compute_gst')
    gst_amount = fields.Float(string='GST Amount')
    
    @api.depends('price_unit', 'product_uom_qty', 'tax_id.tax_type', 'tax_id.type_tax_use')
    def _compute_gst(self):
        cgst_total = 0
        sgst_total = 0
        igst_total = 0
        cgst_rate = 0
        sgst_rate = 0
        igst_rate = 0
 
        for rec in self:
            cgst_total = 0
            sgst_total = 0
            igst_total = 0
            for line in rec.tax_id:
                if line.tax_type == 'cgst' and line.type_tax_use == 'sale':
                    cgst_total = cgst_total + line.amount
                if line.tax_type == 'sgst' and line.type_tax_use == 'sale':
                    sgst_total = sgst_total + line.amount
                if line.tax_type == 'igst' and line.type_tax_use == 'sale':
                    igst_total = igst_total + line.amount
                if line.tax_type == 'cgst' and line.type_tax_use == 'purchase':
                    cgst_total = cgst_total + line.amount
                if line.tax_type == 'sgst' and line.type_tax_use == 'purchase':
                    sgst_total = sgst_total + line.amount
                if line.tax_type == 'igst' and line.type_tax_use == 'purchase':
                    igst_total = igst_total + line.amount
                cgst_rate = cgst_total/100
                sgst_rate = sgst_total/100
                igst_rate = igst_total/100
 
            base = rec.price_unit * (1 - (rec.discount or 0.0) / 100.0)
            rec.cgst = (base * rec.product_uom_qty) * cgst_rate
            rec.sgst = (base * rec.product_uom_qty) * sgst_rate
            rec.igst = (base * rec.product_uom_qty) * igst_rate
            rec.amount = (base * rec.product_uom_qty) + rec.cgst + rec.sgst + rec.igst
#             rec.gst_amount = gst_amt

    
    
