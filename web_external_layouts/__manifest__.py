# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Web External Layouts',
    'category': 'Hidden',
    'version': '1.0',
    'description':
        """
New External Layouts.
========================

This module provides the new external report layouts.
        """,
    'depends': ['web'],
    # 'auto_install': True,
    'data': [
        # 'security/ir.model.access.csv',
        'views/webclient_templates.xml',
        'views/report_templates.xml',
        # 'data/res_company.xml',
        'data/report_layout.xml',
    ],
}
