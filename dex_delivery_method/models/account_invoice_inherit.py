
from odoo import api, fields, models
from odoo.exceptions import UserError, RedirectWarning, ValidationError


class AccountInvoiceInherit(models.Model):
    _inherit = "account.invoice"
    
    
    
    
    @api.model
    def create(self, vals):
        res = super(AccountInvoiceInherit,self).create(vals)
        for invoice in res:
#             print"========res",res,"======vals",vals
#             print"=======invoices ====",invoice.invoice_ids
#             print"==========vals",vals['invoice_line_ids'][0]
            print"=========context",self._context
#             print"=========self._context('active_model')",self._context['active_model']
            if ('active_model' in self._context) and ('active_id' in self._context):
                if self._context['active_model'] == 'purchase.order':
                    if self._context['active_id']:
    #                     id = vals['invoice_line_ids'][0][2]['purchase_id']
                        purchase_id = self.env['purchase.order'].browse(self._context['active_id'])
        #                 print"=====purchase_id",purchase_id
        #                 print"=========",purchase_id.invoice_ids
                        if purchase_id.additional_charges_ids:
                            if purchase_id.pol_additional_chrg_line_ids:
                                if len(purchase_id.invoice_ids) ==1:
                                    for add_charge_id in purchase_id.pol_additional_chrg_line_ids:
            #                             print"add_charge_id",add_charge_id
                                        account = self.env['account.invoice.line'].get_invoice_line_account(invoice.type, add_charge_id.product_id, invoice.fiscal_position_id, invoice.company_id)
            #                             print"account",account
                                        ail = {
                                                'name': add_charge_id.name,
                                                'sequence': invoice.invoice_line_ids[-1].sequence + 1,
                                                'account_id': account.id,
                                                'price_unit': add_charge_id.price_unit,
                                                'quantity': add_charge_id.schduled_delivered_quantity,
                                                'discount': add_charge_id.discount,
            #                                         'uom_id': add_charge_id.product_id.uom_id.id,
                                                'product_id': add_charge_id.product_id.id or False,
#                                                 'invoice_line_tax_ids': [(6, 0, add_charge_id.tax_id.ids)],
                                                'invoice_id': invoice.id,
#                                                 'sequence':invoice.invoice_line_ids[-1].sequence + 1
                                                }
                                        
                                        print"===ail",ail
                                        if ail['price_unit']>0:
                                            id = self.env['account.invoice.line'].create(ail)
                                            id._onchange_product_id()
    #                                     id = self.env['account.invoice.line'].create(ail)
#                                         for inv_line in invoice.invoice_line_ids:
                                            
#                                             id.compute_taxes()
                                            
#                                         print"===ad",id
#                                     if any(line.invoice_line_tax_ids for line in invoice.invoice_line_ids) and not invoice.tax_line_ids:
                                    invoice.compute_taxes()
                                else:
                                    for add_charge_id in purchase_id.pol_additional_chrg_line_ids:
            #                             product_present = False
                                        old_invoice = self.env['account.invoice'].search([('id','in',purchase_id.invoice_ids.ids)],order='date_invoice desc')
                                        print"old_invoice",old_invoice
                                        print"old_invoice",old_invoice[1]
                                        
                                        
                                        for inv_line in old_invoice[1].invoice_line_ids:
                                            if inv_line.product_id == add_charge_id.product_id:
                                                if inv_line.price_unit <= add_charge_id.price_unit:
                                                    account = self.env['account.invoice.line'].get_invoice_line_account(invoice.type, add_charge_id.product_id, invoice.fiscal_position_id, invoice.company_id)
                                                    ail = {
                                                            'name': add_charge_id.name,
#                                                             'sequence': add_charge_id.sequence,
                                                            'account_id': account.id,
                                                            'price_unit': (add_charge_id.price_unit - inv_line.price_unit),
                                                            'quantity': add_charge_id.schduled_delivered_quantity,
                                                            'discount': add_charge_id.discount,
                        #                                         'uom_id': add_charge_id.product_id.uom_id.id,
                                                            'product_id': add_charge_id.product_id.id or False,
#                                                             'invoice_line_tax_ids': [(6, 0, add_charge_id.tax_id.ids)],
                                                                                            
                                                            'invoice_id': invoice.id,
                                                            'sequence':invoice.invoice_line_ids[-1].sequence + 1
                                                            }
                                                    
                                                    print"===ail",ail
                                                    if ail['price_unit']>0:
                                                        id = self.env['account.invoice.line'].create(ail)
                                                        id._onchange_product_id()
                                    
#                                     if any(line.invoice_line_tax_ids for line in invoice.invoice_line_ids) :
#                                         invoice.compute_taxes()
                                    invoice.compute_taxes()            
            #                         raise UserError("ok")
            
            
                if self._context['active_model'] == 'sale.order':
                    if self._context['active_id']:
    #                     id = vals['invoice_line_ids'][0][2]['purchase_id']
                        sale_id = self.env['sale.order'].browse(self._context['active_id'])
                        
                        if sale_id.sol_additional_chrg_line_ids:
                            if len(sale_id.invoice_ids) ==1:
                                for add_charge_id in sale_id.sol_additional_chrg_line_ids:
                                    account = add_charge_id.product_id.property_account_income_id or add_charge_id.product_id.categ_id.property_account_income_categ_id
                                    if not account:
                                        raise UserError(_('Please define income account for this product: "%s" (id:%d) - or for its category: "%s".') %
                                            (add_charge_id.product_id.name, add_charge_id.product_id.id, add_charge_id.product_id.categ_id.name))
                              
                                    fpos = add_charge_id.so_additional_chrg_id.fiscal_position_id or add_charge_id.so_additional_chrg_id.partner_id.property_account_position_id
                                    if fpos:
                                        account = fpos.map_account(account)
                                          
                                        ail = {
                                                'name': add_charge_id.name,
#                                                 'sequence': invoice.invoice_line_ids[-1].sequence + 1,
                                                'account_id': account.id,
                                                'price_unit': add_charge_id.price_unit,
                                                'quantity': add_charge_id.qty_delivered,
                                                'discount': add_charge_id.discount,
                                                'uom_id': add_charge_id.product_uom.id,
                                                'product_id': add_charge_id.product_id.id or False,
                                                'invoice_line_tax_ids': [(6, 0, add_charge_id.product_id.taxes_id.ids)],
                                                'invoice_id': invoice.id
                                                }
                          
                                        print"===ail",ail
                                        if ail['price_unit']>0:
                                            id = self.env['account.invoice.line'].create(ail)
                                            id._onchange_product_id()
                                            id.price_unit= add_charge_id.price_unit
                        
                                invoice.compute_taxes()
                                            
                            else:
#                     
                                for add_charge_id in sale_id.sol_additional_chrg_line_ids:
                                     
                                    old_invoice = self.env['account.invoice'].search([('id','in',sale_id.invoice_ids.ids)],order='date_invoice desc')
#                                    print"old_invoice",old_invoice
 #                                   print"old_invoice",old_invoice[1]
                                                 
                                                 
                                    for inv_line in old_invoice[1].invoice_line_ids:
                                        if inv_line.product_id == add_charge_id.product_id:
                                            if inv_line.price_unit <= add_charge_id.price_unit:
                                     
                                                account = add_charge_id.product_id.property_account_income_id or add_charge_id.product_id.categ_id.property_account_income_categ_id
                                                if not account:
                                                    raise UserError(_('Please define income account for this product: "%s" (id:%d) - or for its category: "%s".') %
                                                        (add_charge_id.product_id.name, add_charge_id.product_id.id, add_charge_id.product_id.categ_id.name))
                                           
                                                fpos = add_charge_id.so_additional_chrg_id.fiscal_position_id or add_charge_id.so_additional_chrg_id.partner_id.property_account_position_id
                                                if fpos:
                                                    account = fpos.map_account(account)
                                                    print("====add_charge_id.price_unit",add_charge_id.price_unit)
                                                    print("====inv_line.price_unit",inv_line.price_unit)
                                                    ail = {
                                                            'name': add_charge_id.name,
#                                                             'sequence': invoice.invoice_line_ids[-1].sequence + 1,
                                                            'account_id': account.id,
                                                            'price_unit': (add_charge_id.price_unit - inv_line.price_unit),
                                                            'quantity': add_charge_id.qty_delivered,
                                                            'discount': add_charge_id.discount,
                                                            'uom_id': add_charge_id.product_uom.id,
                                                            'product_id': add_charge_id.product_id.id or False,
                                                            'invoice_line_tax_ids': [(6, 0, add_charge_id.product_id.taxes_id.ids)],
                                                            'invoice_id': invoice.id,
#                                                             'sequence':invoice.invoice_line_ids[-1].sequence + 1
                                                            }
                                       
            #                                         print"===ail",ail
                                                    if ail['price_unit']>0:
                                                        id = self.env['account.invoice.line'].create(ail)
                                                        print("===========taxes",invoice.tax_line_ids)
                                                        id._onchange_product_id()
                                                        id.price_unit= add_charge_id.price_unit - inv_line.price_unit
                                invoice.compute_taxes()    
        return res
