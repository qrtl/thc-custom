from odoo import fields, models


class StockQuant(models.Model):
    _inherit = "stock.quant"

    value = fields.Monetary(groups="stock_security_adjust.group_stock_officer")
