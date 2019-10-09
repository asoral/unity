from odoo import api, fields, models,_
from odoo.exceptions import UserError, ValidationError
from datetime import datetime

class PurchaseOrder(models.Model):
    _inherit = "purchase.order"
    
    
    additional_charges_ids = fields.One2many('additional.charges','purchase_order_id', string="Additional Charges Ids",copy=True)
    
    pol_additional_chrg_line_ids = fields.One2many('pol.additional.charges','po_additional_chrg_id',string="POL Additional charges IDs")
    
    @api.multi
    def set_additional_charges(self):
        print"=================ok=======set_additional_charges"
        
        for order in self:
            for line in order.additional_charges_ids:
                    carrier = line.carrier_id
                    if line:
                        total_order_qty = total_del_qty = 0
#                         if order.state not in ('draft', 'send','to_approve','purchase'):
#                             raise UserError(_('The order state have to be draft to add Purchase lines.'))
         
#                         carrier = line.carrier_id.verify_carrier(order.partner_shipping_id)
#                         print "----------- carrier line -----------------",carrier
#                         if not carrier:
#                             raise UserError(_('No carrier matching.'))
                        
                        
                        print"order===",order
                        if line.carrier_id.delivery_type == 'fixed':
                            ordered_qty = delivered_qty = 0
                            if line.purchase_order_id:
                                for o in line.purchase_order_id.order_line:
                                    print"qty",o.qty_received
                                    if o.add_charge_applicable == True:
                                        ordered_qty += o.product_qty
                                        if line.carrier_id.based_on == 'deliverd_qty':
                                            if o.qty_received > 0.0:              
                                                delivered_qty += o.qty_received
                                        else:
                                            delivered_qty += o.product_qty 
                            delivered_total=(line.delivery_price/ordered_qty)*delivered_qty
                            print"=======delivered_qty",delivered_qty,"===line.delivery_price",line.delivery_price,"===ordered_qty",ordered_qty
                        
                        if line.carrier_id.delivery_type == 'base_on_rule':
                            if line.carrier_id.based_on == 'ordered_qty':
                                delivered_total = line.carrier_id.get_price_available_custom_ordered_qty(line.purchase_order_id)
                            else:
                                delivered_total = line.carrier_id.get_price_available_custom_delivered_qty(line.purchase_order_id)
                        if line.carrier_id.delivery_type == 'base_on_percent':
                            amt = 0.0
                            l=line.percent
                            if line.purchase_order_id:
                                for o in line.purchase_order_id.order_line:
                                    print"qty",o.qty_received
                                    if o.add_charge_applicable == True:
                                        if line.carrier_id.based_on == 'deliverd_qty':
                                            if o.qty_received > 0.0:
                                                amt += (o.price_unit * o.qty_received)
                                            print"order line",o
                                        else:        
                                            amt += (o.price_unit * o.product_qty)
                            
                            f_amount = amt*(l/100)
                            print "+++++++++++++ final amount",f_amount
                            delivered_total=f_amount
                            print"=======amt",amt,"===o.price_unit",o.price_unit,"===ordered_qty",ordered_qty
                        print"-    ",delivered_total
                        
                        order._create_purchase_line(order,line,delivered_total)
                        
                    else:
                        raise UserError(_('No carrier set for this order.'))    
        return True
        
        
    
    
    @api.multi
    def _create_purchase_line(self, po,aci,delivered_total):
        self.ensure_one()
        

#         taxes = self.product_id.supplier_taxes_id
#         fpos = po.fiscal_position_id
#         taxes_id = fpos.map_tax(taxes) if fpos else taxes
#         if taxes_id:
#             taxes_id = taxes_id.filtered(lambda x: x.company_id.id == self.company_id.id)
        taxes_id = aci.carrier_id.product_id.mapped('taxes_id')
        check = False
        for o_line in self.pol_additional_chrg_line_ids:
            if aci.carrier_id.product_id == o_line.product_id:
                o_line.price_unit =  delivered_total
                return True
            else:
                check = True
                
        if check == True or not self.pol_additional_chrg_line_ids:
            id = self.env['pol.additional.charges'].create({
                'name': aci.carrier_id.name,
                'product_qty': 1,
                'product_id': aci.carrier_id.product_id.id,
                'product_uom': aci.carrier_id.product_id.uom_id.id,
                'price_unit': delivered_total,
#                 'date_planned':datetime.now() ,
                'tax_id': [(6, 0, taxes_id.ids)],
                'po_additional_chrg_id': po.id,
                'schduled_delivered_quantity':1,
                'add_charge_applicable':False
            })
        
        
        print"------------------id",id
        return True
        
    @api.multi
    def reset_additional_charges(self):
        print"=================ok=======reset_additional_charges"
        for order in self:
            order.reset_delivery_price()
            
            
            
    @api.multi
    def reset_delivery_price(self):
        print"***********compute_delivery_price***********"
        for order in self:
            for c_id in order.additional_charges_ids:
                if order.state != 'draft':
                    continue
                if c_id.carrier_id.delivery_type == 'fixed' or c_id.carrier_id.delivery_type == 'base_on_rule':
                    c_id.delivery_price = c_id.carrier_id.with_context(order_id=order.id).price
                    print"_______rule base____________",c_id.delivery_price       
                
                if c_id.carrier_id.delivery_type == 'base_on_percent':
                    print ""      
                    c_id.percent=c_id.carrier_id.percent
                    print"_______percent base____________",c_id.percent
    
    
    
#     -------------method overriden---------------    
    
    @api.multi
    def _create_picking(self):
        StockPicking = self.env['stock.picking']
        for order in self:
            if any([ptype in ['product', 'consu'] for ptype in order.order_line.mapped('product_id.type')]):
                pickings = order.picking_ids.filtered(lambda x: x.state not in ('done','cancel'))
                if not pickings:
                    res = order._prepare_picking()
                    picking = StockPicking.create(res)
                else:
                    picking = pickings[0]
                    
#                 -------------sid---------------

                for add_chrg in order.additional_charges_ids:
                    add_chrg.picking_id = picking.id

#                 -------------sid---------------
                moves = order.order_line._create_stock_moves(picking)
                moves = moves.filtered(lambda x: x.state not in ('done', 'cancel')).action_confirm()
                seq = 0
                for move in sorted(moves, key=lambda move: move.date_expected):
                    seq += 5
                    move.sequence = seq
                moves.force_assign()
                picking.message_post_with_view('mail.message_origin_link',
                    values={'self': picking, 'origin': order},
                    subtype_id=self.env.ref('mail.mt_note').id)
        return True
        
#     -------------method overriden---------------    
    
    
class PurchaseOrderLineInherit(models.Model):
    _inherit = "purchase.order.line"
     
    add_charge_applicable = fields.Boolean(string="Additional Charge Applicable",default=True)
    
    

class POL_Additional_charges(models.Model):
    _name  = "pol.additional.charges"
    
    sequence = fields.Integer(string='Sequence')
    
    po_additional_chrg_id = fields.Many2one('purchase.order',string="PO Additional charges ID")
    
    name = fields.Char(string='Name')
    product_qty = fields.Float('Product Qty')
    product_id = fields.Many2one('product.product',string="Product ID")
    price_unit = fields.Float(string='Unit Price')
    tax_id = fields.Many2many('account.tax',string='Taxes')
    
    schduled_delivered_quantity = fields.Float(string='Quantity Delivered')
    add_charge_applicable = fields.Boolean(string='Additional Charges applicable')
    
    product_uom = fields.Many2one('product.uom',string='Product UOM')
    is_delivery = fields.Boolean(string='Delivery')
    discount = fields.Float(string='Discount')
    
    cgst = fields.Float(string='CGST', compute='_compute_gst', store=True)
    sgst = fields.Float(string='SGST', compute='_compute_gst')
    igst = fields.Float(string='IGST', compute='_compute_gst')
    amount = fields.Float(string='Amt. with Taxes', readonly=True, compute='_compute_gst')
    gst_amount = fields.Float(string='GST Amount')
    
    @api.depends('price_unit', 'product_qty', 'tax_id.tax_type', 'tax_id.type_tax_use')
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
            rec.cgst = (base * rec.product_qty) * cgst_rate
            rec.sgst = (base * rec.product_qty) * sgst_rate
            rec.igst = (base * rec.product_qty) * igst_rate
            rec.amount = (base * rec.product_qty) + rec.cgst + rec.sgst + rec.igst
#             rec.gst_amount = gst_amt

    
    
