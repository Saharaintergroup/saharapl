# -*- coding: utf-8 -*-

from dateutil.relativedelta import relativedelta
from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.addons import decimal_precision as dp


class CustomersPaymentsSales(models.Model):
    _name = 'sales.customers.payments'
    _description = 'Sales Customers Payments'
    company_id = fields.Many2one('res.company', related='journal_id.company_id', string='Company', readonly=True)
    name = fields.Char('Name', readonly=True , default=lambda x: str('New')) #default=default_randint_value
    state = fields.Selection([('draft', 'Draft'), ('confirmed', 'Confirmed'), ('sent', 'Sent'), ('reconciled', 'Reconciled'), ('cancelled', 'Cancelled')], readonly=True, default='draft', copy=False, string="Status")
    order_id = fields.Many2one('sale.order', string='Sale order')
    order_ref = fields.Char('Order Ref') #default=default_randint_value
    partner_id = fields.Many2one('res.partner', string='Customer', required=True)
    amount = fields.Monetary(string='Payment Amount', required=True)
    currency_id = fields.Many2one('res.currency', string='Currency', required=True, default=lambda self: self.env.user.company_id.currency_id)
    payment_date = fields.Date(string='Payment Date', default=fields.Date.context_today, required=True, copy=False)
    communication = fields.Char(string='Memo', compute='oderupdate')
    journal_id = fields.Many2one('account.journal', string='Payment Journal', required=True, domain=[('for_sales_use', '=', True)])
    payment_trans = fields.Char(string='Payment Transaction')
    group_id = fields.Char( readonly=True , default=lambda x: 0)
    procurement_group_id = fields.Many2one('procurement.group', 'Procurement Group', copy=False)
    order_ids = fields.Many2many('sale.order', string='connector order')

    @api.onchange('order_ref')
    def oderupdate(self):
        allorders = self.env['sale.order']
        all_order = allorders.search([])
        for allxr in all_order:
            if self.order_ref == allxr.name :
                self.order_id = allxr.id

    @api.model
    def default_get(self, fields):
        rec = super(CustomersPaymentsSales, self).default_get(fields)
        order_defaults = self.resolve_2many_commands('order_ids', rec.get('order_ids'))
        if order_defaults and len(order_defaults) == 1:
            order = order_defaults[0]
            rec['currency_id'] = order['currency_id'][0]
            rec['partner_id'] = order['partner_id'][0]
            rec['amount'] = order['amount_total']
            rec['order_ref'] = order['name']
        return rec

    @api.one
    def ConfirmPost(self):
        self.write({
            'state': 'confirmed'
            })


class Sales(models.Model):
    _name = 'sale.order'
    _inherit = 'sale.order'

    payments_ids = fields.One2many('sales.customers.payments', 'order_id', 'Payments')
    payments_id = fields.Many2one('sales.customers.payments', string='connector Payments')
    payment_count = fields.Char(string='Coustomer Payments', compute='_compute_payments_ids')
    procurement_group_id = fields.Many2one(
        'procurement.group', 'Procurement Group',
        copy=False)



    state = fields.Selection([
        ('draft', 'Quotation'),
        ('sent', 'Quotation Sent'),
        ('sale', 'Sales Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled'),
        ('unpaid', 'Unpaid'),
        ('partially', 'Partially Paid'),
        ('paid', 'Paid'),
        ], string='Status', readonly=True, copy=False, index=True, track_visibility='onchange', track_sequence=3, default='draft', compute='onchange_calculate_total')





    @api.multi
    def onchange_calculate_total(self):
        for order in self:
            paytotal = self.env['sales.customers.payments'].search([('order_id', '=', order.id)])
            if paytotal:
                payamount = 0;
                for att in paytotal:
                    payamount += float(att.amount)
                    if payamount == 0:
                        order.state = 'unpaid'
                    if payamount != 0 and payamount < order.amount_total:
                        order.state = 'partially'
                    if payamount >= order.amount_total:
                        order.state = 'paid'

    @api.multi
    @api.depends('procurement_group_id')
    def _compute_payments_ids(self):
        for order in self:
            order.payments_ids = self.env['sales.customers.payments'].search([('id', '=', order.procurement_group_id.id)]) if order.procurement_group_id else []
            order.payment_count = len(order.payments_ids)


    @api.multi
    def action_view_payments(self):
        payments = self.mapped('payments_ids')
        action = self.env.ref('sales_customers_payments.action_customers_payments').read()[0]
        return action






class AccountJournalBool(models.Model):
    _name = 'account.journal'
    _inherit = 'account.journal'

    for_sales_use = fields.Boolean('For Sales Use', default=False)

