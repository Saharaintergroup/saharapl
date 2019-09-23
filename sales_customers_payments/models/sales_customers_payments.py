# -*- coding: utf-8 -*-

from dateutil.relativedelta import relativedelta
from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.addons import decimal_precision as dp


class CustomersPaymentsSales(models.Model):
    _name = 'sales.customers.payments'
    _inherits = {'sale.order': 'partner_id'}
    _description = "Sales Customers Payments"




    company_id = fields.Many2one('res.company', related='journal_id.company_id', string='Company', readonly=True)
    name = fields.Char(readonly=True, copy=False) # The name is attributed upon post()
    state = fields.Selection([('draft', 'Draft'), ('confirmed', 'Confirmed'), ('sent', 'Sent'), ('reconciled', 'Reconciled'), ('cancelled', 'Cancelled')], readonly=True, default='draft', copy=False, string="Status")

    partner_id = fields.Many2one('sale.order', string='Sale Order', required=True)

    amount = fields.Monetary(string='Payment Amount', required=True)
    currency_id = fields.Many2one('res.currency', string='Currency', required=True, default=lambda self: self.env.user.company_id.currency_id)
    payment_date = fields.Date(string='Payment Date', default=fields.Date.context_today, required=True, copy=False)
    communication = fields.Char(string='Memo')
    journal_id = fields.Many2one('account.journal', string='Payment Journal', required=True, domain=[('type', 'in', ('bank', 'cash'))])
    payment_trans = fields.Char(string='Payment Transaction')
