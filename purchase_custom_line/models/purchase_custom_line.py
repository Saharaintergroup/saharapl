# -*- coding: utf-8 -*-

from dateutil.relativedelta import relativedelta
from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.addons import decimal_precision as dp


class PurchaseCustomOrderLine(models.Model):
    _name = 'purchase.order.line'
    _inherit = 'purchase.order.line'

    initial_price_unit = fields.Float(string='Initial Unit Price', digits=dp.get_precision('Product Price'))
    support = fields.Float(string='Support', digits=dp.get_precision('Product Price'))

    @api.onchange('initial_price_unit','support')
    def onchange_partner_recipient(self):
        self.price_unit = self.initial_price_unit - self.support
