{
    'name' : 'Metal Weight Calculator',
    'version' : '10.3 updated 13/Sep',
    'summary': '',
    'sequence': 30,
    'description': """
                    updated by smehata 29/7/19 
                    updated by smehata 29/6/19 open lenght and weight field in stock_quant
                    make calculation easy..
                    updayed by sangita 13/09/2019 by task TASK1228

    """,
    "author": "Dexciss Technology Pvt Ltd.(@Ragini)",
   
    "depends": ['product','stock','purchase'],
    "data": [
            "views/metal_weight_cal.xml",
            "views/purchase_order_view.xml",
            "views/stock_picking_view.xml"
            ],
    "installable": True
}
