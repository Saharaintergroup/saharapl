from odoo import models, fields,api

class PurchaseSalesStatus(models.Model):
	_name = "sales.status"
	_description = "New Sales Status"
	name = fields.Char("Sales Status");
	

class PurchaseProcurementStatus(models.Model):
	_name = "procurement.status"
	_description = "New Procurement Status"
	name = fields.Char("Procurement Status");



class PurchaseSalesProcurementStatus(models.Model):
	_inherit = "purchase.requisition"

	purchase_sales_status = fields.Many2one('sales.status',string="Sales Status");
	purchase_procurement_status = fields.Many2one('procurement.status',string="Procurement Status");

