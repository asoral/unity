from odoo import api, fields, models, _

class WizardSalesFormatReport(models.TransientModel):
    _name = 'wizard.sales.format.report'
    
    @api.depends('date_range')
    @api.onchange('date_range','date_from','date_to')
    def get_dates(self):
        for s in self:
            if s.date_range:
                s.date_from = s.date_range.date_start
                s.date_to = s.date_range.date_end
                
    date_range = fields.Many2one('date.range','Date range')
    date_from = fields.Date(string="Date From",required=True)
    date_to = fields.Date(string="Date To",required=True)
    company_id =fields.Many2one('res.company', string="Company", default=lambda self:self.env.user.company_id.id)
    partner_ids = fields.Many2many('res.partner',string="Customer")
    sales_person_ids = fields.Many2many('res.users',string='Sales Person')
    product_ids = fields.Many2many('product.product',string='product')
    area_wise = fields.Selection([
                                  ('state','State')
                                ],string="Area")
#     city_id = fields.Many2one('',string="City")
    state_id = fields.Many2one('res.country.state',string="State")
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
    
    @api.multi
    def button_export_pdf_report(self):
        self.confirm_wizard_sales_format()
        return self.env['report'].get_action(self, 'sales_report_format.sales_report_pdf_format_template_id')
    
    @api.multi
    def get_all_data(self):
        return self.env['sales.format.report'].search([])
    
    @api.multi
    def wizard_date(self):
        str_data = ''
        if self.date_from and self.date_to:
            str_data = 'SO'
        if self.sales_person_ids:
            str_data = 'Sales Person'
        if self.partner_ids:
            str_data = 'Customr'
        if self.product_ids:
            str_data = 'Product'
        if self.state:
            str_data = 'State'
        return str_data

   
    @api.multi
    def confirm_wizard_sales_format(self):
        sales_format_id=self.env['sales.format.report'].search([])
        sales_format_id.unlink()
        domain = []
        query= self.get_query()
        self.env.cr.execute(query)
        res = self.env.cr.dictfetchall()
        for record in res:
            vals = self.get_vals(record)
            rest = sales_format_id.create(vals)
            
        if self.product_ids:
#             
            return {
                'name': 'Sales Format Report',
                'view_type': 'form',
                'view_mode': 'tree',
                'res_model': 'sales.format.report',
                'type': 'ir.actions.act_window',
                'nodestory': True,
                'target': 'current',
                'context':{
                            'search_default_pro_id': True,
                                }
                }
        elif self.partner_ids:
        
            return {
                'name': 'Sales Format Report',
                'view_type': 'form',
                'view_mode': 'tree',
                'res_model': 'sales.format.report',
                'type': 'ir.actions.act_window',
                'nodestory': True,
                'target': 'current',
                'context':{
                            'search_default_partner_id': True,
                                }
                }
            
        elif self.sales_person_ids:
            
            return {
                'name': 'Sales Format Report',
                'view_type': 'form',
                'view_mode': 'tree',
                'res_model': 'sales.format.report',
                'type': 'ir.actions.act_window',
                'nodestory': True,
                'target': 'current',
                'context':{
                            'search_default_user': True,
                                }
                }
            
        elif self.state_id:
            
            return {
                'name': 'Sales Format Report',
                'view_type': 'form',
                'view_mode': 'tree',
                'res_model': 'sales.format.report',
                'type': 'ir.actions.act_window',
                'nodestory': True,
                'target': 'current',
                'context':{
                            'search_default_state_ids': True,
                                }
                }
            
        elif self.state == 'draft' or self.state == 'sent' or self.state == 'proforma_inv' or self.state == 'fst_approval' or self.state == 'snd_approval' or self.state == 'pro'  or self.state == 'blanket_order' or self.state == 'sale' or self.state == 'done' or self.state == 'cancel' or self.state == 'revised' :
            
            return {
                'name': 'Sales Format Report',
                'view_type': 'form',
                'view_mode': 'tree',
                'res_model': 'sales.format.report',
                'type': 'ir.actions.act_window',
                'nodestory': True,
                'target': 'current',
                'context':{
                            'search_default_status': True,
                                }
            }
        else:
            
            return {
                'name': 'Sales Format Report',
                'view_type': 'form',
                'view_mode': 'tree',
                'res_model': 'sales.format.report',
                'type': 'ir.actions.act_window',
                'nodestory': True,
                'target': 'current',
                'context':{
                            'search_default_order': True,
                                }
                }
            
        
    def get_vals(self, record):
        
        vals = {
            "order_no": record.get('order'),
            "order_date": record.get('date'),
            "party_name":record.get('customer'),
            "wo_no": record.get('workorder'),
            "product_id":record.get('product'),
            "user_id":record.get('user'),
            "order_qty": record.get('totalqty'),
            "pending_qty":record.get('pendingqty'),
            "rate":record.get('avgprice'),
            "discount":record.get('discount'),
            "discount_amt": record.get('discountamt'),
            "discount_order_amt": record.get('disorderamt'),
            "pending_amt": record.get('pendingamt'),
            "state":record.get('state'),
            "state_id":record.get('state_id')
            
        }
        return  vals
        
        
        
    def get_query(self):
        from_date = fields.Date.from_string(self.date_from)
        to_date = fields.Date.from_string(self.date_to)
        query="""
           select so.id as order,
            so.date_order as date,
            so.state as state,
            so.state_id as state_id,
            so.partner_id as customer,
            so.user_id as user,
            sol.work_order_no as workorder,
            pp.id as product,
            sum(sol.product_uom_qty) as totalqty,
            sum(sol.qty_delivered) as deliveredqty,
            sum(sol.product_uom_qty  - sol.qty_delivered) as pendingqty,
            avg(sol.price_unit) as avgprice,
            sum(sol.discount) as discount,
            avg((sol.qty_delivered * sol.price_unit) * sol.discount / 100) as discountamt,
            avg((sol.product_uom_qty * sol.price_unit)* sol.discount / 100) as orderamt,
            avg((sol.product_uom_qty * sol.price_unit) - ((sol.product_uom_qty * sol.price_unit)* sol.discount / 100) ) as disorderamt,
            avg(((sol.product_uom_qty  - sol.qty_delivered) * sol.price_unit) - (((sol.product_uom_qty  - sol.qty_delivered) * sol.price_unit) * sol.discount / 100)) as pendingamt
            --avg()
            
            from sale_order_line as sol
            inner join sale_order as so on sol.order_id = so.id
            inner join res_country_state as rcs on so.state_id = rcs.id
            inner join product_product as pp on sol.product_id = pp.id
            inner join product_template as pt on pp.product_tmpl_id = pt.id
            where
                so.date_order BETWEEN  '{}'""".format(from_date)+""" and '{}'""".format(to_date)+"""
                

        """
        
        
                
        if self.partner_ids:
            partner_ids = [t for t in self.partner_ids.ids]
            if len(partner_ids)==1:
                query += " and so.partner_id = {} ".format((partner_ids[0]))
            else:
                query +=" and so.partner_id in {} ".format(tuple(partner_ids))
                
        if self.product_ids:
            product_ids = [t for t in self.product_ids.ids]
            if len(product_ids)==1:
                query += " and pp.id = {} ".format((product_ids[0]))
            else:
                query +=" and pp.id in {} ".format(tuple(product_ids))
            
        if self.sales_person_ids:
            sales_person_ids = [t for t in self.sales_person_ids.ids]
            if len(sales_person_ids)==1:
                query += " and so.user_id = {} ".format((sales_person_ids[0]))
            else:
                query +=" and so.user_id in {} ".format(tuple(sales_person_ids))

        if self.state_id:
            state_ids = [t for t in self.state_id.ids]
            if len(state_ids)==1:
                query += " and so.state_id = {} ".format((state_ids[0]))
            else:
                query +=" and so.state_id in {} ".format(tuple(state_ids))
        
        
        if self.state == 'draft':
            query += "and so.state ='draft'"
        
        if self.state == 'sent':
            query += "and so.state ='sent'"
            
        if self.state == 'proforma_inv':
            query += "and so.state ='proforma_inv'"
            
        if self.state == 'fst_approval':
            query += "and so.state ='fst_approval'"
            
        if self.state == 'snd_approval':
            query += "and so.state ='snd_approval'"
            
        if self.state == 'pro':
            query += "and so.state ='pro'"
            
        if self.state == 'blanket_order':
            query += "and so.state ='blanket_order'"
            
        if self.state == 'sale':
            query += "and so.state ='sale'"
    
        if self.state == 'done':
            query += "and so.state ='done'"
            
        if self.state == 'cancel':
            query += "and so.state ='cancel'"
            
        if self.state == 'revised':
            query += "and so.state ='revised'"
        
        query +=""" group by pp.id,
                    so.id,
                    so.state_id,
                    so.state,
                    so.user_id,
                    so.partner_id,
                    sol.work_order_no
                    """
        return query
        

        
