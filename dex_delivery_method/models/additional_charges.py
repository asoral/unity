
from odoo import api, fields, models,_
from odoo.exceptions import UserError, ValidationError

class Additional_charges(models.Model):
    _name  = "additional.charges" 
    
    
    
    @api.depends('percent','delivery_price','total')
    def get_total(self):
        for res in self:
            if res.carrier_id and res.carrier_id.delivery_type == 'fixed':
                res.total=res.delivery_price
            
            if res.carrier_id and res.carrier_id.delivery_type == 'base_on_rule':
                if res.additonal_id:
                    res.total=res.carrier_id.get_price_available_custom_ordered_qty(res.additonal_id)
                
                if res.purchase_order_id:
                    res.total=res.carrier_id.get_price_available_custom_ordered_qty(res.purchase_order_id)
                    
            if res.carrier_id and res.carrier_id.delivery_type == 'base_on_percent':
#                 print "**********per*********",res.percent
                l=res.percent
                amt = 0.0
                if res.additonal_id:
                    for sol in  res.additonal_id.order_line:
                        print"1"
                        if sol.add_charge_applicable == True:
                            print"2"
                            amt += (sol.price_subtotal)
#                         amt = c_id.additonal_id.amount_untaxed
                if res.purchase_order_id:
                    for sol in  res.purchase_order_id.order_line:
                        print"1"
                        if sol.add_charge_applicable == True:
                            print"2"
                            amt += (sol.price_subtotal)
#                 if res.additonal_id:
#                     amt = res.additonal_id.amount_untaxed
#                 if res.purchase_order_id:
#                     amt = res.purchase_order_id.amount_untaxed1
                    
                f_amount = amt*(l/100)
#                 print "+++++++++++++ final amount",f_amount
                res.total=f_amount
    
    
#     @api.depends('percent','delivery_price','total')
#     def get_total(self):
#         self.get_data()
    
    
    
    
    additonal_id = fields.Many2one('sale.order')   
    picking_id = fields.Many2one('stock.picking')   
    delivery_price = fields.Float(string='Fixed Delivery Price')
    carrier_id = fields.Many2one("delivery.carrier", string="Delivery Type")
    percent = fields.Float(string="Percent(%)")
    total = fields.Float(string="Total" , readonly=True, compute='get_total')
    delivery_type = fields.Selection(related="carrier_id.delivery_type", string="Related", store =  True)
    tax_id = fields.Many2many('account.tax',string='Taxes')

    purchase_order_id = fields.Many2one('purchase.order',string="Purchase Order Id")
    
    delivered_total = fields.Float(string="Delivered Total")
    
    @api.onchange('carrier_id')
    def onchange_carrier_id(self):
#         print"***********compute_delivery_price***********"
        for c_id in self:
                if c_id.carrier_id.delivery_type == 'fixed':  
                    c_id.delivery_price = c_id.carrier_id.fixed_price
                    print"_______fixed____________",c_id.delivery_price       
                
                if c_id.carrier_id.delivery_type == 'base_on_rule':
                    if c_id.additonal_id:
                        c_id.delivery_price = c_id.carrier_id.get_price_available_custom_ordered_qty(c_id.additonal_id)
                    
                    if c_id.purchase_order_id:
                        c_id.delivery_price = c_id.carrier_id.get_price_available_custom_ordered_qty(c_id.purchase_order_id)
                        
                if c_id.carrier_id.product_id.taxes_id:
                    c_id.tax_id =  c_id.carrier_id.product_id.taxes_id.ids    
                    
                if c_id.carrier_id.delivery_type == 'base_on_percent':
                    print "" 
                    l=c_id.percent
                    amt = 0.0
                    if c_id.additonal_id:
                        for sol in  c_id.additonal_id.order_line:
                            if sol.add_charge_applicable == True:
                                amt += (sol.price_subtotal)
#                         amt = c_id.additonal_id.amount_untaxed
                    if c_id.purchase_order_id:
                        for sol in  c_id.purchase_order_id.order_line:
                            print"1"
                            if sol.add_charge_applicable == True:
                               print"2" 
                               amt += (sol.price_subtotal) 
#                         amt = c_id.purchase_order_id.amount_untaxed
                    f_amount = amt*(l/100)
    #                 print "+++++++++++++ final amount",f_amount
                    c_id.total=f_amount     
                    c_id.percent=c_id.carrier_id.percent
                    print"_______percent base____________",c_id.percent
