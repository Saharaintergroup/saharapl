# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Stock Deliveryslip Add Note',
    'category': 'Stock',
    'version': '1.0',
    'description':
        """
Add Note to Deliveryslip
===========================
This module modifies the account addon to add Note to the Deliveryslip
        """,
    'depends': ['stock','web'],
    'auto_install': True,
    'data': [
        'report/report_deliveryslip_note.xml',
    ],
    'application': True,
}

