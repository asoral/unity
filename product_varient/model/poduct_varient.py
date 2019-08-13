
from odoo import api, fields, models, _

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"
    
    prod_temp_id = fields.Many2one('product.template',string="Product",required=True)
    attribute_id = fields.Many2one('product.attribute',string="Attribute")
    value_ids = fields.Many2one('product.attribute.value',string="Attribute Value",required=True)
    
    @api.onchange('prod_temp_id')
    def onchange_prod_temp_id(self):
        for s in self:
            for line in s.prod_temp_id.attribute_line_ids:
                s.attribute_id = line.attribute_id.id
                
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



