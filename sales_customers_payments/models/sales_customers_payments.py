# -*- coding: utf-8 -*-

from dateutil.relativedelta import relativedelta
from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.addons import decimal_precision as dp


class CustomersPaymentsSales(models.Model):
    _name = 'sales.customers.payments'

    company_id = fields.Many2one('res.company', related='journal_id.company_id', string='Company', readonly=True)
    name = fields.Char('ID', readonly=True , default=lambda x: str('New')) #default=default_randint_value
    state = fields.Selection([('draft', 'Draft'), ('confirmed', 'Confirmed'), ('sent', 'Sent'), ('reconciled', 'Reconciled'), ('cancelled', 'Cancelled')], readonly=True, default='draft', copy=False, string="Status")
    order_id = fields.Many2one('sale.order', string='Sale order', required=True)
    partner_id = fields.Many2one('res.partner', string='Customer', required=True)
    amount = fields.Monetary(string='Payment Amount', required=True)
    currency_id = fields.Many2one('res.currency', string='Currency', required=True, default=lambda self: self.env.user.company_id.currency_id)
    payment_date = fields.Date(string='Payment Date', default=fields.Date.context_today, required=True, copy=False)
    communication = fields.Char(string='Memo')
    journal_id = fields.Many2one('account.journal', string='Payment Journal', required=True, domain=[('for_sales_use', '=', True)])
    payment_trans = fields.Char(string='Payment Transaction')
    group_id = fields.Char( readonly=True , default=lambda x: 0)
    procurement_group_id = fields.Many2one('procurement.group', 'Procurement Group', copy=False)

    @api.onchange('order_id')
    def onchange_partner_order(self):
        for res in self.order_id:
        	self.partner_id = res.partner_id



    @api.multi
    def _prepare_procurement_values(self, group_id=False):
        """ Prepare specific key for moves or other components that will be created from a stock rule
        comming from a sale order line. This method could be override in order to add other custom key that could
        be used in move/po creation.
        """
        values = super(SaleOrderLine, self)._prepare_procurement_values(group_id)
        self.ensure_one()
        date_planned = self.order_id.confirmation_date\
            + timedelta(days=self.customer_lead or 0.0) - timedelta(days=self.order_id.company_id.security_lead)
        values.update({
            'company_id': self.order_id.company_id,
            'group_id': group_id,
            'sale_line_id': self.id,
            'date_planned': date_planned,
            'route_ids': self.route_id,
            'warehouse_id': self.order_id.warehouse_id or False,
            'partner_id': self.order_id.partner_shipping_id.id,
        })
        for line in self.filtered("order_id.commitment_date"):
            date_planned = fields.Datetime.from_string(line.order_id.commitment_date) - timedelta(days=line.order_id.company_id.security_lead)
            values.update({
                'date_planned': fields.Datetime.to_string(date_planned),
            })
        return values


class Sales(models.Model):
    _name = 'sale.order'
    _inherit = 'sale.order'

    payments_ids = fields.Many2many('sales.customers.payments', compute='_compute_payments_ids')
    payment_count = fields.Integer(string='Coustomer Payments', compute='_compute_payments_ids')


    @api.multi
    @api.depends('procurement_group_id')
    def _compute_payments_ids(self):
        for order in self:
            order.payments_ids = self.env['sales.customers.payments'].search([('id', '=', order.procurement_group_id.id)]) if order.procurement_group_id else []
            order.payment_count = len(order.picking_ids)


    @api.multi
    def action_view_payments(self):
        payments = self.mapped('payments_ids')
        action = self.env.ref('sales_customers_payments.action_customers_payments').read()[0]
        return action

class AccountJournal(models.Model):
    _name = 'account.journal'
    _inherit = 'account.journal'

    for_sales_use = fields.Boolean('For Sales Use')

