
{
    'name': 'Sales Report Format',
    'version': '10.0.0.3',
    'sequence':1,
    'category': '',
    'description': """
        App will print Sales Report Format.
    """,
    'author': 'Dexciss Technology Pvt. Ltd. (Sangita)',
    'summary': 'App will print Sales Report Format.',
    'website': 'http://www.dexciss.com/',
    'images': [],
    'depends': ['sale','product','product_brand_analysis','sales_team'],
    'data': [
            'wizard/sales_report_format_view_wizard.xml',
            'report/sales_report_pdf_format_template_view.xml',
            'report/sales_report_pdf_format_view.xml',
            'view/sales_report_format.xml',
            ],
                        
    'installable': True,
    'application': True,
    'auto_install': False,
}

