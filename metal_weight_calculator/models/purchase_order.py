from odoo import models,fields,api,_
import odoo.addons.decimal_precision as dp

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

