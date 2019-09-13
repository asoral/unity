from odoo import models,fields,api,_
import odoo.addons.decimal_precision as dp
from odoo.tools.float_utils import float_is_zero, float_compare

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    weight = fields.Float(string='Weight(in Kg)',digits=dp.get_precision('Stock Weight'))
    length = fields.Float(string='Length(in mm)',digits=dp.get_precision('Stock Weight'))
    type = fields.Selection([('length','Length'),
                             ('weight','Weight')] ,string='Calculate',default='length')

    is_eng_product = fields.Boolean(string='Engineering Product', default=False)

    @api.onchange('product_id')
    def set_is_eng_product(self):
        if self:
            if self.product_id.is_eng_product:
                self.is_eng_product =True
            else:
                self.is_eng_product=False


    @api.onchange('type','length','weight')
    def _get_value_from_formula(self):
        for res in self:
            if res.product_id:
                if res.length > 0 and res.type=='length':
                    if res.product_id.material == 'carbon':
                        if res.product_id.shape == 'sheet_plate':
                            if res.product_id.thickness < 0.01:
                                res.weight = 0.00
                            else:
                                weight = 0.000001 * 7860 * res.product_id.thickness * res.product_id.width * res.length
                                res.weight = weight / 1000
                        if res.product_id.shape == 'round':
                            if res.product_id.diameter < 0.001:
                                res.weight = 0.00
                            else:
                                d = res.product_id.diameter
                                weight = 0.00000079 * 7800 * res.length * (d * d)
                                res.weight = weight / 1000

                        if res.product_id.shape == 'square_bar':
                            if res.product_id.across_flats < 0.0001:
                                res.weight = 0.00
                            else:
                                af = res.product_id.across_flats
                                weight = (0.000001 * 7860 * res.length * (af * af))
                                res.weight = weight / 1000


                        if res.product_id.shape == 'hex_bar':
                            if res.product_id.across_flats < 0.0001:
                                res.weight = 0.00
                            else:
                                af = res.product_id.across_flats

                                weight = (0.000000866 * 7800 * res.length * (af * af))
                                res.weight = weight / 1000

                        if res.product_id.shape == 'oct_bar':
                            if res.product_id.across_flats < 0.0001:
                                res.weight = 0.00
                            else:
                                af = res.product_id.across_flats
                                weight = (0.0000008284 * 7800 * res.length * (af * af))
                                res.weight = weight / 1000

                        if res.product_id.shape == 'angle_bar':
                            if res.product_id.thickness < 0.0001:
                                res.weight = 0.00
                            else:
                                weight = (0.000001 * (
                                        res.product_id.leg1 + res.product_id.leg2 - res.product_id.thickness) * res.product_id.thickness * 7800 * res.length)
                                res.weight = weight / 1000

                        if res.product_id.shape == 'hollow_bar':
                            if res.product_id.outer_diameter < 0.0001:
                                res.weight = 0.00
                            else:
                                od = res.product_id.outer_diameter
                                id = res.product_id.inner_diameter
                                weight = (0.0000007854 * 7800 * ((od * od) - (id * id)) * res.length)
                                res.weight = weight / 1000

                        if res.product_id.shape == 'round/pipe':
                            if res.product_id.outer_diameter < 0.0001:
                                res.weight = 0.00
                            else:
                                weight = (0.00000314 * 7800 * (
                                            res.product_id.outer_diameter - res.product_id.width) * res.product_id.width * res.length)
                                res.weight = weight / 1000

                        if res.product_id.shape == 'square':
                            if res.product_id.side1 < 0.0001:
                                res.weight = 0.00
                            else:
                                weight = (0.000001 * (
                                            res.product_id.side1 + res.product_id.side2 - 2 * res.product_id.width) * 2 * res.product_id.width * res.length * 7800)
                                res.weight = weight / 1000

                    # ************************* start for second material**********************

                    elif res.product_id.material == 'austenitic':
                        if res.product_id.shape == 'sheet_plate':
                            if res.product_id.thickness < 0.01:
                                res.weight = 0.00
                            else:
                                weight = 0.000001 * 7900 * res.product_id.thickness * res.product_id.width * res.length
                                res.weight = weight / 1000

                        if res.product_id.shape == 'round':
                            if res.product_id.diameter < 0.001:
                                res.weight = 0.00
                            else:
                                d = res.product_id.diameter
                                weight = 0.00000079 * 7900 * res.length * (d * d)
                                res.weight = weight / 1000

                        if res.product_id.shape == 'square_bar':
                            if res.product_id.across_flats < 0.0001:
                                res.weight = 0.00
                            else:
                                af = res.product_id.across_flats
                                weight = (0.000001 * 7900 * res.length * (af * af))
                                res.weight = weight / 1000

                        if res.product_id.shape == 'hex_bar':
                            if res.product_id.across_flats < 0.0001:
                                res.weight = 0.00
                            else:
                                af = res.product_id.across_flats
                                weight = (0.000000866 * 7900 * res.length * (af * af))
                                res.weight = weight / 1000

                        if res.product_id.shape == 'oct_bar':
                            if res.product_id.across_flats < 0.0001:
                                res.weight = 0.00
                            else:
                                af = res.product_id.across_flats
                                weight = (0.0000008284 * 7900 * res.length * (af * af))
                                res.weight = weight / 1000


                        if res.product_id.shape == 'angle_bar':
                            if res.product_id.thickness < 0.0001:
                                res.weight = 0.00
                            else:
                                weight = (0.000001 * (
                                        res.product_id.leg1 + res.product_id.leg2 - res.product_id.thickness) * res.product_id.thickness * 7900 * res.length)
                                res.weight = weight / 1000

                        if res.product_id.shape == 'hollow_bar':
                            if res.product_id.outer_diameter < 0.0001:
                                res.weight = 0.00
                            else:
                                od = res.product_id.outer_diameter
                                id = res.product_id.inner_diameter
                                weight = (0.0000007854 * 7900 * ((od * od) - (id * id)) * res.length)
                                res.weight = weight / 1000

                        if res.product_id.shape == 'round/pipe':
                            if res.product_id.outer_diameter < 0.0001:
                                res.weight = 0.00
                            else:
                                weight = (0.00000314 * 7900 * (
                                        res.product_id.outer_diameter - res.product_id.width) * res.product_id.width * res.length)
                                res.weight = weight / 1000

                        if res.product_id.shape == 'square':
                            if res.product_id.side1 < 0.0001:
                                res.weight = 0.00
                            else:
                                weight = (0.000001 * (
                                        res.product_id.side1 + res.product_id.side2 - 2 * res.product_id.width) * 2 * res.product_id.width * res.length * 7900)
                                res.weight = weight / 1000

                    # ************************************Third material**************************************
                    elif res.product_id.material == 'copper':
                        if res.product_id.shape == 'sheet_plate':
                            if res.product_id.thickness < 0.01:
                                res.weight = 0.00
                            else:
                                weight = 0.000001 * 8470 * res.product_id.thickness * res.product_id.width * res.length
                                res.weight = weight / 1000

                        if res.product_id.shape == 'round':
                            if res.product_id.diameter < 0.001:
                                res.weight = 0.00
                            else:
                                d = res.product_id.diameter
                                weight = 0.00000079 * 8470 * res.length * (d * d)
                                res.weight = weight / 1000

                        if res.product_id.shape == 'square_bar':
                            if res.product_id.across_flats < 0.0001:
                                res.weight = 0.00
                            else:
                                af = res.product_id.across_flats
                                weight = (0.000001 * 8470 * res.length * (af * af))
                                res.weight = weight / 1000

                        if res.product_id.shape == 'hex_bar':
                            if res.product_id.across_flats < 0.0001:
                                res.weight = 0.00
                            else:
                                af = res.product_id.across_flats
                                weight = (0.000000866 * 8470 * res.length * (af * af))
                                res.weight = weight / 1000

                        if res.product_id.shape == 'oct_bar':
                            if res.product_id.across_flats < 0.0001:
                                res.weight = 0.00
                            else:
                                af = res.product_id.across_flats
                                weight = (0.0000008284 * 8470 * res.length * (af * af))
                                res.weight = weight / 1000


                        if res.product_id.shape == 'angle_bar':
                            if res.product_id.thickness < 0.0001:
                                res.weight = 0.00
                            else:
                                weight = (0.000001 * (
                                            res.product_id.leg1 + res.product_id.leg2 - res.product_id.thickness) * res.product_id.thickness * 7900 * res.length)
                                res.weight = weight / 1000


                        if res.product_id.shape == 'hollow_bar':
                            if res.product_id.outer_diameter < 0.0001:
                                res.weight = 0.00
                            else:
                                od = res.product_id.outer_diameter
                                id = res.product_id.inner_diameter
                                weight = (0.0000007854 * 8470 * ((od * od) - (id * id)) * res.length)
                                res.weight = weight / 1000

                        if res.product_id.shape == 'round/pipe':
                            if res.product_id.outer_diameter < 0.0001:
                                res.weight = 0.00
                            else:
                                weight = (0.00000314 * 8470 * (
                                            res.product_id.outer_diameter - res.product_id.width) * res.product_id.width * res.length)
                                res.weight = weight / 1000

                        if res.product_id.shape == 'square':
                            if res.product_id.side1 < 0.0001:
                                res.weight = 0.00
                            else:
                                weight = (0.000001 * (
                                            res.product_id.side1 + res.product_id.side2 - 2 * res.product_id.width) * 2 * res.product_id.width * res.length * 8470)
                                res.weight = weight / 1000

                    # ******************************************** for 4th material*****************************
                    elif res.product_id.material == 'aluminium':
                        if res.product_id.shape == 'sheet_plate':
                            if res.product_id.thickness < 0.01:
                                res.weight = 0.00
                            else:
                                weight = 0.000001 * 2700 * res.product_id.thickness * res.product_id.width * res.length
                                res.weight = weight / 1000


                        if res.product_id.shape == 'round':
                            if res.product_id.diameter < 0.001:
                                res.weight = 0.00
                            else:
                                d = res.product_id.diameter
                                weight = 0.00000079 * 2700 * res.length * (d * d)
                                res.weight = weight / 1000

                        if res.product_id.shape == 'square_bar':
                            if res.product_id.across_flats < 0.0001:
                                res.weight = 0.00
                            else:
                                af = res.product_id.across_flats
                                weight = (0.000001 * 2700 * res.length * (af * af))
                                res.weight = weight / 1000


                        if res.product_id.shape == 'hex_bar':
                            if res.product_id.across_flats < 0.0001:
                                res.weight = 0.00
                            else:
                                af = res.product_id.across_flats
                                weight = (0.000000866 * 2700 * res.length * (af * af))
                                res.weight = weight / 1000


                        if res.product_id.shape == 'oct_bar':
                            if res.product_id.across_flats < 0.0001:
                                res.weight = 0.00
                            else:
                                af = res.product_id.across_flats
                                weight = (0.0000008284 * 2700 * res.length * (af * af))
                                res.weight = weight / 1000


                        if res.product_id.shape == 'angle_bar':
                            if res.product_id.thickness < 0.0001:
                                res.weight = 0.00
                            else:
                                weight = (0.000001 * (
                                            res.product_id.leg1 + res.product_id.leg2 - res.product_id.thickness) * res.product_id.thickness * 2700 * res.length)
                                res.weight = weight / 1000

                        if res.product_id.shape == 'hollow_bar':
                            if res.product_id.outer_diameter < 0.0001:
                                res.weight = 0.00
                            else:
                                od = res.product_id.outer_diameter
                                id = res.product_id.inner_diameter
                                weight = (0.0000007854 * 2700 * ((od * od) - (id * id)) * res.length)
                                res.weight = weight / 1000


                        if res.product_id.shape == 'round/pipe':
                            if res.product_id.outer_diameter < 0.0001:
                                res.weight = 0.00
                            else:
                                weight = (0.00000314 * 2700 * (
                                            res.product_id.outer_diameter - res.product_id.width) * res.product_id.width * res.length)
                                res.weight = weight / 1000


                        if res.product_id.shape == 'square':
                            if res.product_id.side1 < 0.0001:
                                res.weight = 0.00
                            else:
                                weight = (0.000001 * (
                                            res.product_id.side1 + res.product_id.side2 - 2 * res.product_id.width) * 2 * res.product_id.width * res.length * 2700)
                                res.weight = weight / 1000


                    # ********************************** for 5th material**************************
                    elif res.product_id.material == 'other':

                        if res.product_id.shape == 'sheet_plate':
                            if res.product_id.thickness < 0.01:
                                res.weight = 0.00
                            else:
                                weight = 0.000001 * 5000 * res.product_id.thickness * res.product_id.width * res.length
                                res.weight = weight / 1000

                        if res.product_id.shape == 'round':
                            if res.product_id.diameter < 0.001:
                                res.weight = 0.00
                            else:
                                d = res.product_id.diameter
                                weight = 0.00000079 * 5000 * res.length * (d * d)
                                res.weight = weight / 1000


                        if res.product_id.shape == 'square_bar':
                            if res.product_id.across_flats < 0.0001:
                                res.weight = 0.00
                            else:
                                af = res.product_id.across_flats
                                weight = (0.000001 * 5000 * res.length * (af * af))
                                res.weight = weight / 1000


                        if res.product_id.shape == 'hex_bar':
                            if res.product_id.across_flats < 0.0001:
                                res.weight = 0.00
                            else:
                                af = res.product_id.across_flats
                                weight = (0.000000866 * 5000 * res.length * (af * af))
                                res.weight = weight / 1000


                        if res.product_id.shape == 'oct_bar':
                            if res.product_id.across_flats < 0.0001:
                                res.weight = 0.00
                            else:
                                af = res.product_id.across_flats
                                weight = (0.0000008284 * 5000 * res.length * (af * af))
                                res.weight = weight / 1000


                        if res.product_id.shape == 'angle_bar':
                            if res.product_id.thickness < 0.0001:
                                res.weight = 0.00
                            else:
                                weight = (0.000001 * (
                                            res.product_id.leg1 + res.product_id.leg2 - res.product_id.thickness) * res.product_id.thickness * 5000 * res.length)
                                res.weight = weight / 1000

                        if res.product_id.shape == 'hollow_bar':
                            if res.product_id.outer_diameter < 0.0001:
                                res.weight = 0.00
                            else:
                                od = res.product_id.outer_diameter
                                id = res.product_id.inner_diameter
                                weight = (0.0000007854 * 5000 * ((od * od) - (id * id)) * res.length)
                                res.weight = weight / 1000


                        if res.product_id.shape == 'round/pipe':
                            if res.product_id.outer_diameter < 0.0001:
                                res.weight = 0.00
                            else:
                                weight = (0.00000314 * 5000 * (
                                            res.product_id.outer_diameter - res.product_id.width) * res.product_id.width * res.length)
                                res.weight = weight / 1000

                        if res.product_id.shape == 'square':
                            if res.product_id.side1 < 0.0001:
                                res.weight = 0.00
                            else:
                                weight = (0.000001 * (
                                            res.product_id.side1 + res.product_id.side2 - 2 * res.product_id.width) * 2 * res.product_id.width * res.length * 5000)
                                res.weight = weight / 1000

                elif res.type=='weight' and res.weight > 0:
                    if res.product_id.material == 'carbon':
                        if res.product_id.shape == 'sheet_plate' or res.product_id.shape == 'coil':
                            if res.product_id.thickness < 0.01:
                                res.length = 0.00
                            else:
                                res.length =  (res.weight/(0.000001 * 7860 * res.product_id.thickness * res.product_id.width))*1000

                        if res.product_id.shape == 'round':
                            if res.product_id.diameter < 0.001:
                                res.length = 0.00
                            else:
                                d = res.product_id.diameter
                                res.length = (res.weight / (0.00000079 * 7800 *d * d))*1000

                        if res.product_id.shape == 'square_bar':
                            if res.product_id.across_flats < 0.0001:
                                res.l = 0.00
                            else:
                                af = res.product_id.across_flats
                                res.length = (res.weight / (0.000001 * 7860 * af * af))*1000

                        if res.product_id.shape == 'hex_bar':
                            if res.product_id.across_flats < 0.0001:
                                res.length = 0.00
                            else:
                                af = res.product_id.across_flats
                                res.length = (res.weight / (0.000000866 * 7800 * af * af))*1000

                        if res.product_id.shape == 'oct_bar':
                            if res.product_id.across_flats < 0.0001:
                                res.length = 0.00
                            else:
                                af = res.product_id.across_flats
                                res.length = (res.weight /(0.0000008284 * 7800 * af * af))*1000

                        if res.product_id.shape == 'angle_bar':
                            if res.product_id.thickness < 0.0001:
                                res.length = 0.00
                            else:
                                res.length = (res.weight /(0.000001 * (res.product_id.leg1 + res.product_id.leg2 - res.product_id.thickness) * res.product_id.thickness * 7860))*1000

                        if res.product_id.shape == 'hollow_bar':
                            if res.product_id.outer_diameter < 0.0001:
                                res.length = 0.00
                            else:
                                od = res.product_id.outer_diameter
                                id = res.product_id.inner_diameter
                                res.length = (res.weight / (0.0000007854 * 7800 * ((od * od) - (id * id))))*1000

                        if res.product_id.shape == 'round/pipe':
                            if res.product_id.outer_diameter < 0.0001:
                                res.length = 0.00
                            else:
                                res.length = (res.weight / (0.00000314 * 7800 * (res.product_id.outer_diameter - res.product_id.width) * res.product_id.width))*1000

                        if res.product_id.shape == 'square':
                            if res.product_id.side1 < 0.0001:
                                res.length = 0.00
                            else:
                                res.length = (res.weight / (0.000001 * (res.product_id.side1 + res.product_id.side2 - 2 * res.product_id.width) * 2 * res.product_id.width * 7860))*1000

                        # ************************* start for second material**********************

                    elif res.product_id.material == 'austenitic':
                        # print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! second material"
                        if res.product_id.shape == 'sheet_plate':
                            if res.product_id.thickness < 0.01:
                                res.length = 0.00
                            else:

                                res.length = (res.weight*1000) /(0.000001 * 7900 * res.product_id.thickness * res.product_id.width)

                        if res.product_id.shape == 'round':
                            if res.product_id.diameter < 0.001:
                                res.length = 0.00
                            else:
                                d = res.product_id.diameter
                                res.length = (res.weight*1000) /(0.00000079 * 7900 * (d * d))


                        if res.product_id.shape == 'square_bar':
                            if res.product_id.across_flats < 0.0001:
                                res.length = 0.00
                            else:
                                af = res.product_id.across_flats
                                res.length = (res.weight*1000) / (0.000001 * 7900 * (af * af))

                        if res.product_id.shape == 'hex_bar':
                            if res.product_id.across_flats < 0.0001:
                                res.length = 0.00
                            else:
                                af = res.product_id.across_flats
                                res.length = (res.weight*1000) /(0.000000866 * 7900 * (af * af))

                        if res.product_id.shape == 'oct_bar':
                            if res.product_id.across_flats < 0.0001:
                                res.length = 0.00
                            else:
                                af = res.product_id.across_flats
                                res.length = (res.weight*1000) /(0.0000008284 * 7900 *(af * af))

                        if res.product_id.shape == 'angle_bar':
                            if res.product_id.thickness < 0.0001:
                                res.length = 0.00
                            else:
                                res.length = (res.weight*1000)/(0.000001 * (res.product_id.leg1 + res.product_id.leg2 - res.product_id.thickness) * res.product_id.thickness * 7900)

                        if res.product_id.shape == 'hollow_bar':
                            if res.product_id.outer_diameter < 0.0001:
                                res.weight = 0.00
                            else:
                                od = res.product_id.outer_diameter
                                id = res.product_id.inner_diameter
                                res.length = (res.weight*1000) /(0.0000007854 * 7900 * ((od * od) - (id * id)))

                        if res.product_id.shape == 'round/pipe':
                            if res.product_id.outer_diameter < 0.0001:
                                res.length = 0.00
                            else:
                                res.length = (res.weight*1000) / (0.00000314 * 7900 * (res.product_id.outer_diameter - res.product_id.width) * res.product_id.width )

                        if res.product_id.shape == 'square':
                            if res.product_id.side1 < 0.0001:
                                res.length = 0.00
                            else:
                                res.length = (res.weight*1000) / (0.000001 * (res.product_id.side1 + res.product_id.side2 - 2 * res.product_id.width) * 2 * res.product_id.width)

                    # ************************************Third material**************************************
                    elif res.product_id.material == 'copper':
                        if res.product_id.shape == 'sheet_plate':
                            if res.product_id.thickness < 0.01:
                                res.length = 0.00
                            else:
                                res.length = (res.weight*1000) /(0.000001 * 8470 * res.product_id.thickness * res.product_id.width )

                        if res.product_id.shape == 'coil':
                            if res.product_id.thickness < 0.001:
                                res.length = 0.00
                            else:
                                res.length = (res.weight*1000)/(0.000001 * 8470 * res.product_id.thickness * res.product_id.width)

                        if res.product_id.shape == 'round':
                            if res.product_id.diameter < 0.001:
                                res.length = 0.00
                            else:
                                d = res.product_id.diameter
                                res.length = (res.weight*1000) /(0.00000079 * 8470 * (d * d))


                        if res.product_id.shape == 'square_bar':
                            if res.product_id.across_flats < 0.0001:
                                res.length = 0.00
                            else:
                                af = res.product_id.across_flats
                                res.length = (res.weight /(0.000001 * 8470 * (af * af)))*1000

                        if res.product_id.shape == 'hex_bar':
                            if res.product_id.across_flats < 0.0001:
                                res.length = 0.00
                            else:
                                af = res.product_id.across_flats
                                res.length = (res.weight*1000) /(0.000000866 * 8470 * (af * af))


                        if res.product_id.shape == 'oct_bar':
                            if res.product_id.across_flats < 0.0001:
                                res.length = 0.00
                            else:
                                af = res.product_id.across_flats
                                res.length = (res.weight*1000) /(0.0000008284 * 8470 *(af * af))

                        if res.product_id.shape == 'angle_bar':
                            if res.product_id.thickness < 0.0001:
                                res.length = 0.00
                            else:
                                res.length = (res.weight*1000) /(0.000001 * (res.product_id.leg1 + res.product_id.leg2 - res.product_id.thickness) * res.product_id.thickness * 7900)

                        if res.product_id.shape == 'hollow_bar':
                            if res.product_id.outer_diameter < 0.0001:
                                res.length = 0.00
                            else:
                                od = res.product_id.outer_diameter
                                id = res.product_id.inner_diameter
                                res.length = (res.weight*1000) /(0.0000007854 * 8470 * ((od * od) - (id * id)))

                        if res.product_id.shape == 'round/pipe':
                            if res.product_id.outer_diameter < 0.0001:
                                    res.length = 0.00
                            else:
                                res.length = (res.weight*1000) /(0.00000314 * 8470 * (res.product_id.outer_diameter - res.product_id.width) * res.product_id.width)

                        if res.product_id.shape == 'square':
                            if res.product_id.side1 < 0.0001:
                                res.length = 0.00
                            else:
                                res.length = (res.weight*1000) /(0.000001 * (res.product_id.side1 + res.product_id.side2 - 2 * res.product_id.width) * 2 * res.product_id.width * 8470)

                    # ******************************************** for 4th material*****************************
                    elif res.product_id.material == 'aluminium':
                        if res.product_id.shape == 'sheet_plate':
                            if res.product_id.thickness < 0.01:
                                res.length = 0.00
                            else:
                                res.length = res.weight / (0.000001 * 2700 * res.product_id.thickness * res.product_id.width)
                        if res.product_id.shape == 'round':
                            if res.product_id.diameter < 0.001:
                                res.length = 0.00
                            else:
                                d = res.product_id.diameter
                                res.length = (res.weight*1000) /(0.00000079 * 2700 * (d * d))

                        if res.product_id.shape == 'square_bar':
                            if res.product_id.across_flats < 0.0001:
                                res.length = 0.00
                            else:
                                af = res.product_id.across_flats
                                res.length = (res.weight*1000) /(0.000001 * 2700 * (af * af))

                        if res.product_id.shape == 'hex_bar':
                            if res.product_id.across_flats < 0.0001:
                                res.length = 0.00
                            else:
                                af = res.product_id.across_flats
                                res.length = (res.weight*1000) /(0.000000866 * 2700 * (af * af))

                        if res.product_id.shape == 'oct_bar':
                            if res.product_id.across_flats < 0.0001:
                                res.length = 0.00
                            else:
                                af = res.product_id.across_flats
                                res.weight = (res.weight*1000) /(0.0000008284 * 2700 * (af * af))

                        if res.product_id.shape == 'angle_bar':
                            if res.product_id.thickness < 0.0001:
                                res.length = 0.00
                            else:
                                res.length = (res.weight*1000) /(0.000001 * (res.product_id.leg1 + res.product_id.leg2 - res.product_id.thickness) * res.product_id.thickness * 2700)

                        if res.product_id.shape == 'hollow_bar':
                            if res.product_id.outer_diameter < 0.0001:
                                res.length = 0.00
                            else:
                                od = res.product_id.outer_diameter
                                id = res.product_id.inner_diameter
                                res.length = (res.weight*1000)/(0.0000007854 * 2700 * ((od * od) - (id * id)))

                        if res.product_id.shape == 'round/pipe':
                            if res.product_id.outer_diameter < 0.0001:
                                res.length = 0.00
                            else:
                                res.length =(res.weight*1000) /(0.00000314 * 2700 * (res.product_id.outer_diameter - res.product_id.width) * res.product_id.width)

                        if res.product_id.shape == 'square':
                            if res.product_id.side1 < 0.0001:
                                res.weight = 0.00
                            else:
                                res.length =(res.weight*1000) /(0.000001 * (res.product_id.side1 + res.product_id.side2 - 2 * res.product_id.width) * 2 * res.product_id.width *2700)

                    # ********************************** for 5th material**************************
                    elif res.product_id.material == 'other':
                        if res.product_id.shape == 'sheet_plate':
                            if res.product_id.thickness < 0.01:
                                res.length = 0.00
                            else:
                                res.length = res.weight /(0.000001 * 5000 * res.product_id.thickness * res.product_id.width)

                        if res.product_id.shape == 'round':
                            if res.product_id.diameter < 0.001:
                                res.length = 0.00
                            else:
                                d = res.product_id.diameter
                                res.length = (res.weight*1000) /(0.00000079 * 5000 *(d * d))

                        if res.product_id.shape == 'square_bar':
                            if res.product_id.across_flats < 0.0001:
                                res.length = 0.00
                            else:
                                af = res.product_id.across_flats
                                res.length = (res.weight*1000) /(0.000001 * 5000 *(af * af))

                        if res.product_id.shape == 'hex_bar':
                            if res.product_id.across_flats < 0.0001:
                                res.length = 0.00
                            else:
                                af = res.product_id.across_flats
                                res.length = (res.weight*1000) / (0.000000866 * 5000 *(af * af))

                        if res.product_id.shape == 'oct_bar':
                            if res.product_id.across_flats < 0.0001:
                                res.length = 0.00
                            else:
                                af = res.product_id.across_flats
                                res.length = (res.weight*1000)/(0.0000008284 * 5000 * (af * af))

                        if res.product_id.shape == 'angle_bar':
                            if res.product_id.thickness < 0.0001:
                                res.length = 0.00
                            else:
                                res.length = (res.weight*1000) /(0.000001 * (res.product_id.leg1 + res.product_id.leg2 - res.product_id.thickness) * res.product_id.thickness * 5000)

                        if res.product_id.shape == 'hollow_bar':
                            if res.product_id.outer_diameter < 0.0001:
                                res.length = 0.00
                            else:
                                od = res.product_id.outer_diameter
                                id = res.product_id.inner_diameter
                                res.length = (res.weight*1000) /(0.0000007854 * 5000 * ((od * od) - (id * id)))

                        if res.product_id.shape == 'round/pipe':
                            if res.product_id.outer_diameter < 0.0001:
                                res.length = 0.00
                            else:
                                res.length = (res.weight*1000) /(0.00000314 * 5000 * (
                                        res.product_id.outer_diameter - res.product_id.width) * res.product_id.width)

                        if res.product_id.shape == 'square':
                            if res.product_id.side1 < 0.0001:
                                res.length = 0.00
                            else:
                                res.length = (res.weight*1000) /(0.000001 * (res.product_id.side1 + res.product_id.side2 - 2 * res.product_id.width) * 2 * res.product_id.width * 5000)
                # res.product_qty = res.length
                res.product_qty = res.weight
                
                
    @api.multi
    def _prepare_stock_moves(self, picking):
        """ Prepare the stock moves data for one order line. This function returns a list of
        dictionary ready to be used in stock.move's create()
        """
        print("get core method callllllllllllll",self.length,self.weight,self.type,self.is_eng_product)
        self.ensure_one()
        res = []
        if self.product_id.type not in ['product', 'consu']:
            return res
        qty = 0.0
        price_unit = self._get_stock_move_price_unit()
        for move in self.move_ids.filtered(lambda x: x.state != 'cancel'):
            qty += move.product_qty
        template = {
            'name': self.name or '',
            'product_id': self.product_id.id,
            'product_uom': self.product_uom.id,
            'date': self.order_id.date_order,
            'date_expected': self.date_planned,
            'location_id': self.order_id.partner_id.property_stock_supplier.id,
            'location_dest_id': self.order_id._get_destination_location(),
            'picking_id': picking.id,
            'partner_id': self.order_id.dest_address_id.id,
            'move_dest_id': False,
            'state': 'draft',
            'purchase_line_id': self.id,
            'company_id': self.order_id.company_id.id,
            'price_unit': price_unit,
            'picking_type_id': self.order_id.picking_type_id.id,
            'group_id': self.order_id.group_id.id,
            'procurement_id': False,
            'origin': self.order_id.name,
            'route_ids': self.order_id.picking_type_id.warehouse_id and [(6, 0, [x.id for x in self.order_id.picking_type_id.warehouse_id.route_ids])] or [],
            'warehouse_id': self.order_id.picking_type_id.warehouse_id.id,
            'type':self.type,
            'weight':self.weight,
            'length':self.length,
            'is_eng_product':self.is_eng_product,
        }
        # Fullfill all related procurements with this po line
        diff_quantity = self.product_qty - qty
        for procurement in self.procurement_ids.filtered(lambda p: p.state != 'cancel'):
            # If the procurement has some moves already, we should deduct their quantity
            sum_existing_moves = sum(x.product_qty for x in procurement.move_ids if x.state != 'cancel')
            existing_proc_qty = procurement.product_id.uom_id._compute_quantity(sum_existing_moves, procurement.product_uom)
            procurement_qty = procurement.product_uom._compute_quantity(procurement.product_qty, self.product_uom) - existing_proc_qty
            if float_compare(procurement_qty, 0.0, precision_rounding=procurement.product_uom.rounding) > 0 and float_compare(diff_quantity, 0.0, precision_rounding=self.product_uom.rounding) > 0:
                tmp = template.copy()
                tmp.update({
                    'product_uom_qty': min(procurement_qty, diff_quantity),
                    'move_dest_id': procurement.move_dest_id.id,  # move destination is same as procurement destination
                    'procurement_id': procurement.id,
                    'propagate': procurement.rule_id.propagate,
                })
                res.append(tmp)
                diff_quantity -= min(procurement_qty, diff_quantity)
        if float_compare(diff_quantity, 0.0,  precision_rounding=self.product_uom.rounding) > 0:
            template['product_uom_qty'] = diff_quantity
            res.append(template)
        return res

    @api.multi
    def _create_stock_moves(self, picking):
        moves = self.env['stock.move']
        done = self.env['stock.move'].browse()
        for line in self:
            for val in line._prepare_stock_moves(picking):
                done += moves.create(val)
        return done

