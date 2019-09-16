# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Account Journal Report',
    'category': 'Accounting',
    'version': '1.0',
    'description':
        """
Add Journal payment
===========================
This module modifies the account addon to add Jouranl payment to the Payment Receipt
        """,
    'depends': ['account','web'],
    'auto_install': True,
    'data': [
        'views/report_payment_receipt_templates1.xml',
    ],
    'application': True,
    'license': 'OEEL-1',
}
