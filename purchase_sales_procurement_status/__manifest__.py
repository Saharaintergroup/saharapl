# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Purchase Sales Status',
    'version': '1.0',
    'category': 'Purchases',
    'sequence': 60,
    'summary': 'Purchase orders, tenders and agreements',
    'description': "",
    'website': 'https://www.odoo.com/page/purchase',
    'depends': ['purchase','purchase_requisition'],
    'data': [
        'security/ir.model.access.csv',
        'views/res_config_settings_views.xml',
        'views/status_view.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
