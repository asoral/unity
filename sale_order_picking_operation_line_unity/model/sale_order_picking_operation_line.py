from openerp import api, fields, models, _
from collections import namedtuple
from odoo.tools.float_utils import float_compare



class StockPackOperation(models.Model):
    _inherit = "stock.pack.operation"

    name = fields.Char(string='Description')

 
class StockPicking(models.Model):
    _inherit = "stock.picking"
     
     
    def _prepare_pack_ops(self, quants, forced_qties):
        """ Prepare pack_operations, returns a list of dict to give at create """
        # TDE CLEANME: oh dear ...
        valid_quants = quants.filtered(lambda quant: quant.qty > 0)
#         print"Validqunts------------------------->",valid_quants
        _Mapping1 = namedtuple('Mapping', ('move','product', 'package', 'owner', 'location', 'location_dst_id','name'))
#         _Mapping2 = namedtuple('Mapping', ('move','product', 'package', 'owner', 'location', 'location_dst_id','name'))

        print"------------------------------------------",forced_qties
        all_products = valid_quants.mapped('product_id') | self.env['product.product'].browse(p[0].id for p in forced_qties.keys()) | self.move_lines.mapped('product_id')
        computed_putaway_locations = dict(
            (product, self.location_dest_id.get_putaway_strategy(product) or self.location_dest_id.id) for product in all_products)
        product_to_uom = dict((product.id, product.uom_id) for product in all_products)
        picking_moves = self.move_lines.filtered(lambda move: move.state not in ('done', 'cancel'))
        print"moveidssssssssssssssssssssss++++++++++++++++++++++>",picking_moves
        for move in picking_moves:
            # If we encounter an UoM that is smaller than the default UoM or the one already chosen, use the new one instead.
#             print "move ids for loop is working or not++++++++===============>"
            if move.product_uom != product_to_uom[move.product_id.id] and move.product_uom.factor > product_to_uom[move.product_id.id].factor:
                product_to_uom[move.product_id.id] = move.product_uom
        if len(picking_moves.mapped('location_id')) > 1:
            print"length of picking moves ids------------->"
            raise UserError(_('The source location must be the same for all the moves of the picking.'))
        if len(picking_moves.mapped('location_dest_id')) > 1:
            raise UserError(_('The destination location must be the same for all the moves of the picking.'))
        pack_operation_values = []
        # find the packages we can move as a whole, create pack operations and mark related quants as done
        top_lvl_packages = valid_quants._get_top_level_packages(computed_putaway_locations)
        for pack in top_lvl_packages:
            pack_quants = pack.get_content()
            pack_operation_values.append({
                'picking_id': self.id,
                'package_id': pack.id,
                'product_qty': 1.0,
                'location_id': pack.location_id.id,
                'location_dest_id': computed_putaway_locations[pack_quants[0].product_id],
                'owner_id': pack.owner_id.id,
            })
            valid_quants -= pack_quants
            print"```````````````````````````````````````````````````````````",valid_quants
        # Go through all remaining reserved quants and group by product, package, owner, source location and dest location
        # Lots will go into pack operation lot object
        qtys_grouped = {}
        lots_grouped = {}
        for quant in valid_quants:
            key = _Mapping1(quant.reservation_id,quant.product_id, quant.package_id, quant.owner_id, quant.location_id,computed_putaway_locations[quant.product_id],
                            quant.reservation_id.name)
            qtys_grouped.setdefault(key, 0.0)
            qtys_grouped[key] = quant.qty
            if quant.product_id.tracking != 'none' and quant.lot_id:
                lots_grouped.setdefault(key, dict()).setdefault(quant.lot_id.id, 0.0)
                lots_grouped[key][quant.lot_id.id] = quant.qty
        # Do the same for the forced quantities (in cases of force_assign or incomming shipment for example)
        for product, qty in forced_qties.items():
#            print"productQtyvaluessssssss????????????????????????????????????",product,qty,forced_qties.items()
            if qty <= 0.0:
                continue
            lot = self.env['stock.move'].search([('id','=',product[1])])
            key = _Mapping1(self.id,product, self.env['stock.quant.package'], self.owner_id, self.location_id, computed_putaway_locations[product[0]],
                            lot.name)
            qtys_grouped.setdefault(key, 0.0)
            qtys_grouped[key] = qty
            print"22222222222222222222222222222222222222222",qtys_grouped[key]
        # Create the necessary operations for the grouped quants and remaining qtys
        Uom = self.env['product.uom']
        product_id_to_vals = {}  # use it to create operations using the same order as the picking stock moves
        for mapping, qty in qtys_grouped.items():
            print"???????????????????????????????????????",mapping
            uom = product_to_uom[mapping.product[0].id]
            val_dict = {
                'picking_id': self.id,
                'product_qty': mapping.product[0].uom_id._compute_quantity(qty, uom),
                'product_id': mapping.product[0].id,
                'package_id': mapping.package.id,
                'owner_id': mapping.owner.id,
                'location_id': mapping.location.id,
                'name':mapping.name,
                'location_dest_id': mapping.location_dst_id,
                'product_uom_id': uom.id,
                'pack_lot_ids': [
                    (0, 0, {'lot_id': lot, 'qty': 0.0, 'qty_todo': lots_grouped[mapping][lot]})
                    for lot in lots_grouped.get(mapping, {}).keys()],
            }
            print"((((((((((((((((((((((((((((((((-----------------------",val_dict
            product_id_to_vals.setdefault(mapping.product[0].id, list()).append(val_dict)
        for move in self.move_lines.filtered(lambda move: move.state not in ('done', 'cancel')):
            values = product_id_to_vals.pop(move.product_id.id, [])
            pack_operation_values += values
#            print"[[[[[[[[[[[[[[[[[[[[[[[[[[[pack_operation_values[[[[[[[[[[[[[[[[[[[[[[",pack_operation_values,values
        return pack_operation_values
    
    
    @api.multi
    def do_prepare_partial(self):
        # TDE CLEANME: oh dear ...
        PackOperation = self.env['stock.pack.operation']

        # get list of existing operations and delete them
        existing_packages = PackOperation.search([('picking_id', 'in', self.ids)])  # TDE FIXME: o2m / m2o ?
        if existing_packages:
            existing_packages.unlink()
        for picking in self:
            forced_qties = {}  # Quantity remaining after calculating reserved quants
            picking_quants = self.env['stock.quant']
            # Calculate packages, reserved quants, qtys of this picking's moves
            for move in picking.move_lines:
                if move.state not in ('assigned', 'confirmed', 'waiting'):
                    continue
                move_quants = move.reserved_quant_ids
                picking_quants = move_quants
                print"&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&", picking_quants
                forced_qty = 0.0
                if move.state == 'assigned':
                    qty = move.product_uom._compute_quantity(move.product_uom_qty, move.product_id.uom_id, round=False)
                    forced_qty = qty - sum([x.qty for x in move_quants])
                    print"movequnatsssssssssssssssssssssssssssssssssssss", move_quants,forced_qty
                    # if we used force_assign() on the move, or if the move is incoming, forced_qty > 0
                    #                 if float_compare(forced_qty, 0, precision_rounding=move.product_id.uom_id.rounding) > 0:
                    #                     if forced_qties.get(move.product_id):
                    #                         forced_qties[move.product_id] += forced_qty
                    #                     else:
                    forced_qties[(move.product_id,move.id)] = forced_qty
                    print"/////////////////////////////////////////////////",forced_qty
                    print"^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^", forced_qties
            for vals in picking._prepare_pack_ops(picking_quants, forced_qties):
                # print"((((((((((((((((((((((((((((((((((((((((((((((((("
                vals['fresh_record'] = False
                PackOperation |= PackOperation.create(vals)
                # print"###############################################", vals, PackOperation
        # recompute the remaining quantities all at once
        self.do_recompute_remaining_quantities()
        for pack in PackOperation:
            pack.ordered_qty = sum(
                pack.mapped('linked_move_operation_ids').mapped('move_id').filtered(
                    lambda r: r.state != 'cancel').mapped('ordered_qty')
            )
            print"$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$", pack.ordered_qty
        self.write({'recompute_pack_op': False})
        
        
#     @api.multi
#     def do_new_transfer(self):
#         res = super(StockPicking,self).do_new_transfer()
# 
#         for pack in self.pack_operation_product_ids:
# 
#             reserve_picking_id = self.id
#             reserve_picking_move = self.env['stock.move'].search(
#                 [('picking_id', '=', reserve_picking_id), ('product_id', '=', pack.product_id.id),('name','=',pack.name)])
# 
#             print"do new resfer method caalll move",reserve_picking_id,reserve_picking_move
#             for reserve_move in reserve_picking_move:
#                 # print"Stock move result=====deckle======>>>>", reserve_move, pack
#                 reserve_move.quant_ids.update({
#                     'name':pack.name
#                 })
#                 print"-------new deckle size----------",reserve_move.quant_ids.name,pack
#         return res

        
class InventoryLine(models.Model):
    _inherit = "stock.inventory.line"

    name = fields.Char(string="Description")
    
    
class StockQuant(models.Model):
    _inherit = 'stock.quant'

    name = fields.Char(string="Description")
        
