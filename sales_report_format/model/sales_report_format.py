from odoo import api, fields, models

class SalesFormatReport(models.Model):
    _name='sales.format.report'
    
    order_no = fields.Many2one('sale.order',string="Order No")
    order_date = fields.Date(string="Order Date")
    party_name = fields.Many2one('res.partner',string="Party Name")
    wo_no = fields.Char(string="WO No")
    product_id = fields.Many2one('product.product',string="Product Name")
    user_id = fields.Many2one('res.users',string="User")
    order_qty = fields.Float(string="Order Qty")
    pending_qty = fields.Float(string="Pending Qty")
    rate = fields.Float(string="Rate")
    discount = fields.Float(string="Discount")
    discount_amt = fields.Float(string="Discount Amount")
    discount_order_amt = fields.Float(string="Discount Order Qty")
    pending_amt = fields.Float(string="Pending Amount")
    user_id = fields.Many2one('res.users', string='User', default=lambda self:self.env.user.id)
    company_id = fields.Many2one('res.company', related ="user_id.company_id", string="Company")
    state = fields.Selection([
        ('draft', 'Quotation'),
        ('sent', 'Quotation Sent'),
        ('proforma_inv', 'Proforma Invoice'),
        ('fst_approval', '1st Approval'),
        ('snd_approval', '2nd Approval'),
        ('pro', 'Release Order'),
        ('blanket_order', 'Blanket Order'),
        ('sale', 'Sales Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled'),
        ('revised','Revised')
        ], string='Status')