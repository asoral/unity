
import itertools
import psycopg2

import odoo.addons.decimal_precision as dp

from odoo import api, fields, models, tools, _
from odoo.exceptions import ValidationError, except_orm



class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"
    
    prod_temp_id = fields.Many2one('product.template',string="Product",required=True)
    attribute_id = fields.Many2one('product.attribute',string="Attribute")
    value_ids = fields.Many2one('product.attribute.value',string="Attribute Value")
#     dynamic_domain_ids = fields.Many2many('product.attribute.value',string="Dynamic")
    
    @api.onchange('prod_temp_id')
    def onchange_prod_temp_id(self):
        for s in self:
            for line in s.prod_temp_id.attribute_line_ids:
                s.attribute_id = line.attribute_id.id
            if not s.attribute_id:
                product_id = self.env['product.product'].search([('product_tmpl_id','=',self.prod_temp_id.id)])
#                 print("_______---product_idproduct_idproduct_id-----------------------",product_id)
                for product in product_id:
                    s.product_id = product
                    
            attr = self.env['product.attribute.value']
            for attributes in s.prod_temp_id.attribute_line_ids:
                attr += attributes.mapped('value_ids')
            return {'domain':{'value_ids':[('id','in',attr.ids)]}}
            
    @api.onchange('value_ids')
    def onchange_value_ids(self):
        for s in self:
            for line in s.value_ids.product_ids:
                s.product_id = line.id
                
class ProductAttributeValue(models.Model):
    _inherit = "product.attribute.value"

    prod_temp_id = fields.Many2one('product.template',string="Product")

    @api.model
    def create(self, vals):
        template = super(ProductAttributeValue, self).create(vals)
        val_list = []
        if "create_product_product" not in self._context:
#             print(";;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;",self._context,template,template.prod_temp_id)
            variant_alone = template.prod_temp_id.attribute_line_ids.filtered(lambda line: line.attribute_id.create_variant and len(line.value_ids) == 1).mapped('value_ids')
#             print("[[[[[[[[[[[[[[[[[[[[[[[[[[",vals)
            attri_id = self._context.get('default_attribute_id')
            vals_name = vals.get('name')
#             if not variant_alone:
            for line in template.prod_temp_id.attribute_line_ids:
                
#                 print("3333333333333333",a,line.attribute_id)
                if line.attribute_id.id == attri_id:
                    for value in line.value_ids:
                        val_list.append(value.id)
#                     print("11111111111111111",val_list,vals_name)
                    val_list.append(template.id)
#                     print("2222222222222222222",val_list)
                    line.value_ids = [(6,0,val_list)]
#                     print("333333333333line======>>>",line.value_ids)
                    template.prod_temp_id.create_variant_ids()
#                     print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<",template.prod_temp_id.create_variant_ids())
        return template
#             template.with_context(create_from_tmpl=True).create_variant_ids()

class ProductTemplate(models.Model):
    _inherit = "product.template"

    default_code = fields.Char(
        'Internal Reference', inverse='_set_default_code', store=True)
    
    @api.one
    def _set_default_code(self):
        if self.product_variant_ids:
#             print("mymethoddddddddddddd")
            self.product_variant_ids.default_code = self.default_code

    @api.depends('product_variant_ids', 'product_variant_ids.default_code')
    def _compute_default_code(self):
        for variant in self.product_variant_ids:
            self.default_code = variant.default_code
#             print("???????????????????",self.default_code)
#         return True

    
    @api.multi
    def create_variant_ids(self):
        Product = self.env["product.product"]
        for tmpl_id in self.with_context(active_test=False):
            print("createeeeeee======",tmpl_id.default_code)
            # adding an attribute with only one value should not recreate product
            # write this attribute on every product to make sure we don't lose them
            variant_alone = tmpl_id.attribute_line_ids.filtered(lambda line: len(line.value_ids) == 1).mapped('value_ids')
            for value_id in variant_alone:
                updated_products = tmpl_id.product_variant_ids.filtered(lambda product: value_id.attribute_id not in product.mapped('attribute_value_ids.attribute_id'))
                updated_products.write({'attribute_value_ids': [(4, value_id.id)]})

            # list of values combination
            existing_variants = [set(variant.attribute_value_ids.ids) for variant in tmpl_id.product_variant_ids]
            variant_matrix = itertools.product(*(line.value_ids for line in tmpl_id.attribute_line_ids if line.value_ids and line.value_ids[0].attribute_id.create_variant))
            variant_matrix = map(lambda record_list: reduce(lambda x, y: x+y, record_list, self.env['product.attribute.value']), variant_matrix)
            to_create_variants = filter(lambda rec_set: set(rec_set.ids) not in existing_variants, variant_matrix)

            # check product
            variants_to_activate = self.env['product.product']
            variants_to_unlink = self.env['product.product']
            for product_id in tmpl_id.product_variant_ids:
                if not product_id.active and product_id.attribute_value_ids in variant_matrix:
                    variants_to_activate |= product_id
                elif product_id.attribute_value_ids not in variant_matrix:
                    variants_to_unlink |= product_id
            if variants_to_activate:
                variants_to_activate.write({'active': True})

            # create new product
            for variant_ids in to_create_variants:
                new_variant = Product.create({
                    'product_tmpl_id': tmpl_id.id,
                    'attribute_value_ids': [(6, 0, variant_ids.ids)],
                    'default_code':tmpl_id.default_code
                })
#                 print("==================",new_variant)

            # unlink or inactive product
            for variant in variants_to_unlink:
                try:
                    with self._cr.savepoint(), tools.mute_logger('odoo.sql_db'):
                        variant.unlink()
                # We catch all kind of exception to be sure that the operation doesn't fail.
                except (psycopg2.Error, except_orm):
                    variant.write({'active': False})
                    pass
        return True