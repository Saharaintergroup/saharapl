# -*- coding: utf-8 -*-
{
    'name': "User Restrict Cancellation",
    'author': "Matrix",
    'category': 'Invoicing Management',
    'summary': """This module allow to control restrict user cancellation for Sale Order, Purchase Order, Customer Invoice and Journal Entries.""",
    'version': '12.0.1.0',

    'description': """
        This Module allow to control cancel for customer invoice, vendor bill, customer payment and journal entries.
    """,
    'depends': ['base', 'account', 'sale', 'purchase'],
    'data': ['views/account_invoice_view.xml',
             'security/access_right_view.xml', ],
    'price': 50,
    'sequence': 1,
    'license': 'OPL-1',
    'currency': 'EUR',    
	'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
}
