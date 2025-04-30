from odoo import models, fields


class StockQuant(models.Model):
    _inherit = 'stock.quant'

    value = fields.Monetary(groups='stock_security_adjust.group_stock_officer')
