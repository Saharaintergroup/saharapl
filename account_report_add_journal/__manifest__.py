# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Account Journal Report',
    'category': 'Accounting',
    'version': '1.0',
    'description':
        """
Add Journal payment to Payment Receipt
===========================
This module modifies the account addon to add Jouranl payment to the Payment Receipt
        """,
    'depends': ['base_setup', 'product', 'analytic', 'portal', 'digest','account'],
    'auto_install': True,
    'data': [
        'views/report_payment_receipt_templates1.xml',

    ],
    'qweb': [
        "static/src/xml/*.xml",
    ],
    'license': 'OEEL-1',
}