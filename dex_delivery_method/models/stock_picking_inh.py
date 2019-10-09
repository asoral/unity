from odoo import models, fields, api, _
from odoo.exceptions import UserError
import odoo.addons.decimal_precision as dp

class StockPicking(models.Model):
    _inherit = 'stock.picking'
    
    add_charges_ids = fields.One2many('additional.charges','picking_id', string="Additional Charges", store=True)
    
    
    @api.multi
    def _create_backorder(self, backorder_moves=[]):
        backorder_id = super(StockPicking, self)._create_backorder(backorder_moves=[])
        print"===========backorder",backorder_id
        
        if self.add_charges_ids:
            self._add_delivery_cost_to_so_po()
        
        if self.add_charges_ids:
            for line in self.add_charges_ids:
                print"====add_charges",line
                    
                line.picking_id = backorder_id.id
            
    @api.multi
    def _add_delivery_cost_to_so_po(self):
        print"***************2 method _add_delivery_cost_to_so***********************"
        for l in self.add_charges_ids:
            if l.carrier_id and l.carrier_id.delivery_type not in ['fixed', 'base_on_rule','base_on_percent'] and l.carrier_id.integration_level == 'rate_and_ship':
                l.send_to_shipper()
                print"=============ok=================send_to_shipper="
        print" -----_add_delivery_cost_to_so my-------"
        self.ensure_one()
        sale_order = self.sale_id
        if sale_order.invoice_shipping_on_delivery:
            sale_order.delivery_set_limit()
        
        if self.po_id:
            print"====po",self.po_id
            self.po_id.set_additional_charges()
            
    @api.multi
    def put_in_pack(self):
        # TDE FIXME: work in batch, please
        self.ensure_one()
        package = super(StockPicking, self).put_in_pack()

        current_package_carrier_type = self.carrier_id.delivery_type if self.carrier_id.delivery_type not in ['base_on_rule', 'fixed','base_on_percent'] else 'none'
        count_packaging = self.env['product.packaging'].search_count([('package_carrier_type', '=', current_package_carrier_type)])
        if not count_packaging:
            return False
        # By default, sum the weights of all package operations contained in this package
        pack_operation_ids = self.env['stock.pack.operation'].search([('result_package_id', '=', package.id)])
        package_weight = sum([x.qty_done * x.product_id.weight for x in pack_operation_ids])
        package.shipping_weight = package_weight

        return {
            'name': _('Package Details'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'stock.quant.package',
            'view_id': self.env.ref('delivery.view_quant_package_form_save').id,
            'target': 'new',
            'res_id': package.id,
            'context': {
                'current_package_carrier_type': current_package_carrier_type,
            },
        }   
    
    
class StockMove(models.Model):
    _inherit = 'stock.move'    
      
    @api.multi
    def action_confirm(self):
        """
            Pass the carrier to the picking from the sales order
            (Should also work in case of Phantom BoMs when on explosion the original move is deleted)
        """
 #       print "*********** stock.move core action_confirm **********"
        procs_to_check = []
        for move in self:
#            print"self",move
            if move.procurement_id and move.procurement_id.sale_line_id and move.procurement_id.sale_line_id.order_id.add_charges_ids:
                procs_to_check += [move.procurement_id]
        res = super(StockMove, self).action_confirm()
#        print "^^^^^^^^^^^^^^^^^^^^^^^^^^^^",res,procs_to_check
        for proc in procs_to_check:
#             print"proc.move_ids",proc.move_ids
#             print"proc.move_ids.picking",proc.move_ids.picking_id
            pickings = (proc.move_ids.mapped('picking_id'))
#            print 'PPPPPPPPPPPPPPPPPPPp',pickings,proc.sale_line_id.order_id.add_charges_ids
            
            
            #this need to be implemented for first time of sale order confirm
            if len(pickings)==1:
                if pickings:
                    for line in proc.sale_line_id.order_id.add_charges_ids:
                        line.picking_id=pickings.id
#                     print"***********************",line,line.picking_id
        return res
    
