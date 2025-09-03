# Copyright 2025 Quartile Limited
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.tools import float_is_zero


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    @api.depends("qty_to_receive", "product_uom", "product_id.uom_id")
    def _compute_qty_to_receive_stock_uom(self):
        for line in self:
            if line.product_id and line.product_id.uom_id != line.product_uom:
                line.qty_to_receive_stock_uom = line.product_uom._compute_quantity(line.qty_to_receive, line.product_id.uom_id)
            else:
                line.qty_to_receive_stock_uom = line.qty_to_receive
             

    qty_to_receive_stock_uom = fields.Float(
        compute="_compute_qty_to_receive_stock_uom",
        digits="Product Unit of Measure",
        copy=False,
        string="Qty to Receive (Stock UoM)",
    )