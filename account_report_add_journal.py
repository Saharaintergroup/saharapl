from odoo import models, fields, api,



class account_report_add_journal(models.Model):
	_name = "account.report.add.journal"
    _description = "Add Journal"

    name = fields.Char(translate=True)