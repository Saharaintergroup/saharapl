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
    invoice_ids = fields.Many2many('account.invoice', 'account_invoice_transaction_rel', 'transaction_id', 'invoice_id',
                                   string='Invoices', copy=False, readonly=True)


    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('sales.customers.payments') or _('New')                
            result = super(CustomersPaymentsSales, self).create(vals)
            return result


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

        paymet_send = self.pay_and_reconcile()
        self.write({
            'state': 'confirmed'
            })

    @api.multi
    def _prepare_account_payment_vals(self):
        self.ensure_one()
        return {
            'state': 'draft',
            'amount': self.amount,
            'payment_type': 'inbound',
            'currency_id': self.currency_id.id,
            'partner_id': self.partner_id.id,
            'partner_type': 'customer',
            'invoice_ids': [(6, 0, self.invoice_ids.ids)],
            'journal_id': self.journal_id.id,
            'company_id': self.company_id.id,
            'payment_method_id': self.env.ref('account.account_payment_method_manual_in').id,
            'payment_token_id': None,
            'communication': self.communication,
            'writeoff_account_id': False,
        }


    @api.multi
    def pay_and_reconcile(self):
        payment_vals = self._prepare_account_payment_vals()
        payment = self.env['account.payment'].create(payment_vals)
        payment.postdraft()

        return True

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
        return {
            'name': _('Customer Payments'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'sales.customers.payments',
            'view_id': False,
            'type': 'ir.actions.act_window',
            'domain': [('order_id', 'in', self.ids)],
        }






class AccountJournalBool(models.Model):
    _name = 'account.journal'
    _inherit = 'account.journal'

    for_sales_use = fields.Boolean('For Sales Use', default=False)

class account_payment(models.Model):
    _name = "account.payment"
    _inherit = 'account.payment'


    @api.multi
    def postdraft(self):
        """ Create the journal items for the payment and update the payment's state to 'posted'.
            A journal entry is created containing an item in the source liquidity account (selected journal's default_debit or default_credit)
            and another in the destination reconcilable account (see _compute_destination_account_id).
            If invoice_ids is not empty, there will be one reconcilable move line per invoice to reconcile with.
            If the payment is a transfer, a second journal entry is created in the destination journal to receive money from the transfer account.
        """
        for rec in self:

            if rec.state != 'draft':
                raise UserError(_("Only a draft payment can be posted."))

            if any(inv.state != 'open' for inv in rec.invoice_ids):
                raise ValidationError(_("The payment cannot be processed because the invoice is not open!"))

            # keep the name in case of a payment reset to draft
            if not rec.name:
                # Use the right sequence to set the name
                if rec.payment_type == 'transfer':
                    sequence_code = 'account.payment.transfer'
                else:
                    if rec.partner_type == 'customer':
                        if rec.payment_type == 'inbound':
                            sequence_code = 'account.payment.customer.invoice'
                        if rec.payment_type == 'outbound':
                            sequence_code = 'account.payment.customer.refund'
                    if rec.partner_type == 'supplier':
                        if rec.payment_type == 'inbound':
                            sequence_code = 'account.payment.supplier.refund'
                        if rec.payment_type == 'outbound':
                            sequence_code = 'account.payment.supplier.invoice'
                rec.name = self.env['ir.sequence'].with_context(ir_sequence_date=rec.payment_date).next_by_code(sequence_code)
                if not rec.name and rec.payment_type != 'transfer':
                    raise UserError(_("You have to define a sequence for %s in your company.") % (sequence_code,))

            # Create the journal entry
            amount = rec.amount * (rec.payment_type in ('outbound', 'transfer') and 1 or -1)
            move = rec._create_payment_entry(amount)

            # In case of a transfer, the first journal entry created debited the source liquidity account and credited
            # the transfer account. Now we debit the transfer account and credit the destination liquidity account.
            if rec.payment_type == 'transfer':
                transfer_credit_aml = move.line_ids.filtered(lambda r: r.account_id == rec.company_id.transfer_account_id)
                transfer_debit_aml = rec._create_transfer_entry(amount)
                (transfer_credit_aml + transfer_debit_aml).reconcile()

            rec.write({'state': 'draft', 'move_name': move.name})
        return True
