{
    'name' : 'Dex Delivery Method',
    'version' : '10.0.4',
    'summary': ' Dex Delivery Method',
    'sequence': 30,
    'description': """  updated by sid on 27-2-19 : tax total where coming wrong 
                        updated by sid on 25-2-19 : taxes are properly coming in invoices
                        Updated by sid on 30-1-18 : added functionality for based on rule.
                        Updated by sid on 11-1-19 : added same functionality for purchase order
                        IMP : has overriden the _create_picking method of purchase.order
                        Last updated by sangita Added tax field in additional charges 26/04/2019
			Last Updated by Sangita Error Generate in Create and view Invoice TASK1371
                        this module is created for additional charges in sale and purchase order """,
    'author': "Dexciss Technology Pvt Ltd(@Ragini,Sid)",
   
    "depends": ['purchase','sale','delivery','sale_stock','stock','dex_custom_picking_po'],
    "data": [
            "views/purchase_order_inherit.xml",
            "views/delivery_carrier_view.xml",
            "views/sale_order_inh_view.xml",
            "views/stock_picking_inh.xml"
            ],
    "installable": True,
}
