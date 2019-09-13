from odoo import models, fields, api

class ProductTemplate(models.Model):
    _inherit = "product.template"
    
    material = fields.Selection([
                                ('carbon', 'Carbon & ferritic stainless steels'),
                                ('austenitic', 'Austenitic stainless steels'),
                                ('copper', 'Copper alloys'),
                                ('aluminium', 'Aluminium alloys'),
                                ('other', 'Others'),
                                ],string='Material')
    
    shape = fields.Selection([
                            ('sheet_plate', 'Sheet/plate'),
                            ('coil', 'Coil'),
                            ('round', 'Round/bar/wire'),
                            ('square_bar','Square bar'),
                            ('hex_bar', 'Hex bar'),
                            ('oct_bar', 'Oct bar'),
                            ('angle_bar', 'Angle bar'),
                            ('hollow_bar', 'Hollow bar'),
                            ('round/pipe', 'Round/tube/pipe'),
                            ('square', 'Square/rect'),
                            ],string='Shape')
    
    thickness=fields.Float(string='Thickness(in m)')
    width=fields.Float(string='Width(in mm)')
    length=fields.Float(string='Length(in mm)')
    diameter=fields.Float(string='Diameter(in mm)')
    across_flats=fields.Float(string='Across flats(in mm)')
    leg1=fields.Float(string='Length1(in mm)')
    leg2=fields.Float(string='Length2(in mm)')
    outer_diameter=fields.Float(string='Outer diameter(in mm)')
    inner_diameter=fields.Float(string='Inner diameter(in mm)')
    side1=fields.Float(string='Side1(in mm)')
    side2=fields.Float(string='Side2(in mm)')


    is_eng_product = fields.Boolean(string='Engineering Product',default=False)

    @api.onchange('material','shape','thickness','weight','volume','length','diameter',
                  'across_flats','leg1','leg2','outer_diameter','inner_diameter','side1','side2')
    def onchange_material(self):
        #print "*****************************enter"
        if self.material == 'carbon':
            #print "%%%%%%%%%%%%%%%%%%%%%%%%%%%%second"
            if self.shape == 'sheet_plate':
                if self.thickness < 0.01:
                  self.weight=0.00
                else: 
                  weight=0.000001*7860*self.thickness*self.width*self.length
                  #print "****************************************",  ("%.5f" %(wt/7800))
                  self.volume=(weight/7800)
                  self.weight=weight/1000
                  #print "============= 111========================",weight,self.volume, self.weight
               
            if self.shape == 'coil': 
                if self.thickness < 0.001:
                  self.weight=0.00
                else:
                  weight= 0.000001*7860*self.thickness*self.width 
                  self.weight=weight/1000
                  self.volume=(weight/7800)
                  #print "============= 111========================",weight,self.volume, self.weight  
            if self.shape == 'round':         
                if self.diameter < 0.001:
                  self.weight=0.00   
                else:
                  d=self.diameter
                  weight=0.00000079*7800*self.length*(d*d)   
                  self.weight=weight/1000  
                  self.volume=weight/7800
                  #print "============= 111========================",weight,self.volume, self.weight 
            if self.shape == 'square_bar':         
                if self.across_flats < 0.0001:
                  self.weight=0.00 
                else:
                 af=self.across_flats
                 weight=(0.000001*7860*self.length*(af*af))
                 self.weight=weight/1000 
                 self.volume=(weight/7800)  
                 #print "============= 111========================",weight,self.volume, self.weight   
            if self.shape == 'hex_bar':  
                if self.across_flats < 0.0001:
                    self.weight=0.00
                else:
                  af=self.across_flats
                  #print "*********************************************** hex",af*af
                  weight=(0.000000866*7800*self.length*(af*af)) 
                  self.weight= weight/1000
                  self.volume=(weight/7800) 
                  #print "============= 111========================",weight,self.volume, self.weight
                  
            if self.shape == 'oct_bar':  
                if self.across_flats < 0.0001: 
                     self.weight=0.00     
                else:
                  af=self.across_flats 
                  weight=(0.0000008284*7800*self.length*(af*af))
                  self.weight= weight/1000
                  self.volume=(weight/7800) 
                  #print "============= 111========================",weight,self.volume, self.weight
                  
            if self.shape == 'angle_bar':       
                if self.thickness < 0.0001: 
                     self.weight=0.00       
                else:
                    weight=(0.000001*(self.leg1+self.leg2-self.thickness)*self.thickness*7860*self.length)
                    self.weight=weight/1000
                    self.volume=(weight/7800)
                    #print "============= 111========================",weight,self.volume, self.weight
            if self.shape == 'hollow_bar':     
                if self.outer_diameter < 0.0001: 
                     self.weight=0.00         
                else:
                    od=self.outer_diameter
                    id=self.inner_diameter
                    weight=(0.0000007854*7800*((od*od)-(id*id))*self.length) 
                    self.weight=weight/1000
                    self.volume=(weight/7800)
                    #print "============= 111========================",weight,self.volume, self.weight
            if self.shape == 'round/pipe':     
                if self.outer_diameter < 0.0001: 
                     self.weight=0.00                 
                else:
                    weight=(0.00000314*7800*(self.outer_diameter-self.width)*self.width*self.length)    
                    self.weight=weight/1000
                    self.volume=(weight/7800)
                    #print "============= 111========================",weight,self.volume, self.weight
            if self.shape == 'square':          
                if self.side1 < 0.0001: 
                     self.weight=0.00             
                else:
                    weight=(0.000001*(self.side1+self.side2-2*self.width)*2*self.width*self.length*7860)   
                    self.weight=weight/1000
                    self.volume=(weight/7800)
                    #print "============= 111========================",weight,self.volume, self.weight
    # ************************* start for second material**********************               
        
        elif  self.material == 'austenitic':
            #print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! second material"
            if self.shape == 'sheet_plate':
                if self.thickness < 0.01:
                  self.weight=0.00
                else:
                  weight=0.000001*7900*self.thickness*self.width*self.length 
                  self.weight=weight/1000
                  self.volume=(weight/7900)
           
            if self.shape == 'coil': 
                if self.thickness < 0.001:
                  self.weight=0.00
                else:
                  weight=0.000001*7900*self.thickness*self.width  
                  self.weight= weight/1000
                  self.volume=(weight/7900)
            
            if self.shape == 'round':         
                if self.diameter < 0.001:
                  self.weight=0.00   
                else:
                  d=self.diameter
                  weight=0.00000079*7900*self.length*(d*d) 
                  self.weight= weight/1000
                  self.volume=(weight/7900)
                            
            if self.shape == 'square_bar':         
                if self.across_flats < 0.0001:
                  self.weight=0.00 
                else:
                 af=self.across_flats
                 weight=(0.000001*7900*self.length*(af*af))
                 self.weight=weight/1000
                 self.volume=(weight/7900)    
           
            if self.shape == 'hex_bar':  
                if self.across_flats < 0.0001:
                    self.weight=0.00
                else:
                  af=self.across_flats
                  weight=(0.000000866*7900*self.length*(af*af)) 
                  self.weight= weight/1000
                  self.volume=(weight/7900)
            
            if self.shape == 'oct_bar':  
                if self.across_flats < 0.0001: 
                     self.weight=0.00     
                else:
                  af=self.across_flats
                  weight=(0.0000008284*7900*self.length*(af*af)) 
                  self.weight=weight/1000
                  self.volume=(weight/7900)
            
            if self.shape == 'angle_bar':       
                if self.thickness < 0.0001: 
                     self.weight=0.00       
                else:
                    weight=(0.000001*(self.leg1+self.leg2-self.thickness)*self.thickness*7900*self.length)
                    self.weight=weight/1000
                    self.volume=(weight/7900)
            
            if self.shape == 'hollow_bar':     
                if self.outer_diameter < 0.0001: 
                     self.weight=0.00         
                else:
                    od=self.outer_diameter
                    id=self.inner_diameter
                    weight=(0.0000007854*7900*((od*od)-(id*id))*self.length) 
                    self.weight=weight/1000
                    self.volume=(weight/7900)
            
            if self.shape == 'round/pipe':     
                if self.outer_diameter < 0.0001: 
                     self.weight=0.00                 
                else:
                    weight=(0.00000314*7900*(self.outer_diameter-self.width)*self.width*self.length)    
                    self.weight=weight/1000
                    self.volume=(weight/7900)
            
            if self.shape == 'square':          
                if self.side1 < 0.0001: 
                     self.weight=0.00             
                else:
                    weight=(0.000001*(self.side1+self.side2-2*self.width)*2*self.width*self.length*7900)  
                    self.weight=weight/1000
                    self.volume=(weight/7900)
#************************************Third material**************************************
        elif  self.material == 'copper':            
            if self.shape == 'sheet_plate':
                if self.thickness < 0.01:
                  self.weight=0.00
                else:
                  weight=0.000001*8470*self.thickness*self.width*self.length
                  self.weight= weight/1000
                  self.volume=(weight/8470)
            
            if self.shape == 'coil': 
                if self.thickness < 0.001:
                  self.weight=0.00
                else:
                  weight= 0.000001*8470*self.thickness*self.width
                  self.weight= weight/1000
                  self.volume=(weight/8470)
            
            if self.shape == 'round':         
                if self.diameter < 0.001:
                  self.weight=0.00   
                else:
                  d=self.diameter
                  weight=0.00000079*8470*self.length*(d*d) 
                  self.weight=weight/1000 
                  self.volume=(weight/8470)
            
            if self.shape == 'square_bar':         
                if self.across_flats < 0.0001:
                  self.weight=0.00 
                else:
                 af=self.across_flats
                 weight=(0.000001*8470*self.length*(af*af))
                 self.weight=weight/1000 
                 self.volume=(weight/8470)         
            
            if self.shape == 'hex_bar':  
                if self.across_flats < 0.0001:
                    self.weight=0.00
                else:
                  af=self.across_flats
                  weight=(0.000000866*8470*self.length*(af*af)) 
                  self.weight=weight/1000 
                  self.volume=(weight/8470)
           
            if self.shape == 'oct_bar':  
                if self.across_flats < 0.0001: 
                     self.weight=0.00     
                else:
                  af=self.across_flats
                  weight=(0.0000008284*8470*self.length*(af*af)) 
                  self.weight=weight/1000
                  self.volume=(weight/8470)
            
            if self.shape == 'angle_bar':       
                if self.thickness < 0.0001: 
                     self.weight=0.00       
                else:
                    weight=(0.000001*(self.leg1+self.leg2-self.thickness)*self.thickness*7900*self.length)
                    self.weight=weight/1000
                    self.volume=(weight/8470)
            
            if self.shape == 'hollow_bar':     
                if self.outer_diameter < 0.0001: 
                     self.weight=0.00         
                else:
                    od=self.outer_diameter
                    id=self.inner_diameter
                    weight=(0.0000007854*8470*((od*od)-(id*id))*self.length) 
                    self.weight=weight/1000
                    self.volume=(weight/8470)
            
            if self.shape == 'round/pipe':     
                if self.outer_diameter < 0.0001: 
                     self.weight=0.00                 
                else:
                    weight=(0.00000314*8470*(self.outer_diameter-self.width)*self.width*self.length)    
                    self.weight=weight/1000
                    self.volume=(weight/8470)
            
            if self.shape == 'square':          
                if self.side1 < 0.0001: 
                     self.weight=0.00             
                else:
                    weight=(0.000001*(self.side1+self.side2-2*self.width)*2*self.width*self.length*8470)      
                    self.weight=weight/1000
                    self.volume=(weight/8470)
#******************************************** for 4th material*****************************                    
        elif  self.material == 'aluminium':                
            
            if self.shape == 'sheet_plate':
                if self.thickness < 0.01:
                  self.weight=0.00
                else: 
                  weight= 0.000001*2700*self.thickness*self.width*self.length        
                  self.weight= weight/1000
                  self.volume=(weight/2700)
                    
            if self.shape == 'coil': 
                if self.thickness < 0.001:
                  self.weight=0.00
                else:
                  weight= 0.000001*2700*self.thickness*self.width 
                  self.weight=weight/1000      
                  self.volume=(weight/2700)
            
            if self.shape == 'round':         
                if self.diameter < 0.001:
                  self.weight=0.00   
                else:
                  d=self.diameter
                  weight=0.00000079*2700*self.length*(d*d)
                  self.weight=weight/1000
                  self.volume=(weight/2700)
             
            if self.shape == 'square_bar':         
                if self.across_flats < 0.0001:
                  self.weight=0.00 
                else:
                 af=self.across_flats
                 weight=(0.000001*2700*self.length*(af*af))
                 self.weight=weight/1000
                 self.volume=(weight/2700) 
            
            if self.shape == 'hex_bar':  
                if self.across_flats < 0.0001:
                    self.weight=0.00
                else:
                  af=self.across_flats
                  weight=(0.000000866*2700*self.length*(af*af))
                  self.weight=weight/1000
                  self.volume=(weight/2700)
            
            if self.shape == 'oct_bar':  
                if self.across_flats < 0.0001: 
                     self.weight=0.00     
                else:
                  af=self.across_flats
                  weight=(0.0000008284*2700*self.length*(af*af))  
                  self.weight=weight/1000
                  self.volume=(weight/2700)
           
            if self.shape == 'angle_bar':       
                if self.thickness < 0.0001: 
                     self.weight=0.00       
                else:
                    weight=(0.000001*(self.leg1+self.leg2-self.thickness)*self.thickness*2700*self.length)
                    self.weight=weight/1000
                    self.volume=(weight/2700)
                        
            if self.shape == 'hollow_bar':     
                if self.outer_diameter < 0.0001: 
                     self.weight=0.00         
                else:
                    od=self.outer_diameter
                    id=self.inner_diameter
                    weight=(0.0000007854*2700*((od*od)-(id*id))*self.length) 
                    self.weight=weight/1000
                    self.volume=(weight/2700)
            
            if self.shape == 'round/pipe':     
                if self.outer_diameter < 0.0001: 
                     self.weight=0.00                 
                else:
                    weight=(0.00000314*2700*(self.outer_diameter-self.width)*self.width*self.length)    
                    self.weight=weight/1000
                    self.volume=(weight/2700)
            
            if self.shape == 'square':          
                if self.side1 < 0.0001: 
                     self.weight=0.00             
                else:
                    weight=(0.000001*(self.side1+self.side2-2*self.width)*2*self.width*self.length*2700)
                    self.weight=weight/1000
                    self.volume=(weight/2700)
                    
#********************************** for 5th material************************** 
        elif  self.material == 'other': 
            
            if self.shape == 'sheet_plate':
                if self.thickness < 0.01:
                  self.weight=0.00
                else:
                  weight= 0.000001*5000*self.thickness*self.width*self.length          
                  self.weight=weight/1000
                  self.volume=(weight/5000) 
                    
            if self.shape == 'coil': 
                if self.thickness < 0.001:
                  self.weight=0.00
                else:
                  weight=0.000001*5000*self.thickness*self.width  
                  self.weight=weight/1000
                  self.volume=(weight/5000)

            if self.shape == 'round':         
                if self.diameter < 0.001:
                  self.weight=0.00   
                else:
                  d=self.diameter
                  weight=0.00000079*5000*self.length*(d*d) 
                  self.weight=weight/1000
                  self.volume=(weight/5000)   
                    
            if self.shape == 'square_bar':         
                if self.across_flats < 0.0001:
                  self.weight=0.00 
                else:
                 af=self.across_flats
                 weight=(0.000001*5000*self.length*(af*af)) 
                 self.weight=weight/1000
                 self.volume=(weight/5000)   
                     
            if self.shape == 'hex_bar':  
                if self.across_flats < 0.0001:
                    self.weight=0.00
                else:
                  af=self.across_flats
                  weight=(0.000000866*5000*self.length*(af*af)) 
                  self.weight=weight/1000
                  self.volume=(weight/5000)
                  
                  
            if self.shape == 'oct_bar':  
                if self.across_flats < 0.0001: 
                     self.weight=0.00     
                else:
                  af=self.across_flats 
                  weight= (0.0000008284*5000*self.length*(af*af)) 
                  self.weight=weight/1000
                  self.volume=(weight/5000)
                  
            if self.shape == 'angle_bar':       
                if self.thickness < 0.0001: 
                     self.weight=0.00       
                else:
                    weight=(0.000001*(self.leg1+self.leg2-self.thickness)*self.thickness*5000*self.length)
                    self.weight=weight/1000
                    self.volume=(weight/5000)
                  
                  
            if self.shape == 'hollow_bar':
                if self.outer_diameter < 0.0001: 
                     self.weight=0.00         
                else:
                    od=self.outer_diameter
                    id=self.inner_diameter
                    weight=(0.0000007854*5000*((od*od)-(id*id))*self.length) 
                    self.weight=weight/1000
                    self.volume=(weight/5000)
                    
            if self.shape == 'round/pipe':     
                if self.outer_diameter < 0.0001: 
                     self.weight=0.00                 
                else:
                    weight=(0.00000314*5000*(self.outer_diameter-self.width)*self.width*self.length)    
                    self.weight=weight/1000
                    self.volume=(weight/5000)
                    
            if self.shape == 'square':          
                if self.side1 < 0.0001: 
                     self.weight=0.00             
                else:
                    weight=(0.000001*(self.side1+self.side2-2*self.width)*2*self.width*self.length*5000)   
                    self.weight=weight/1000
                    self.volume=(weight/5000)
                                                                                                                                                           