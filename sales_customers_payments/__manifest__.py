# -*- coding: utf-8 -*-
{
    'name': 'Sales Customers Payments',
    'version': '1.0',
    'category': 'Sales',
    'description': "Add Sales Customers Payments for sales man",
    'depends': ['sale','payment'],
    'data': [
        'security/ir.model.access.csv',
        'views/sales_customers_payments.xml',
    ],
    'installable': True,
}
