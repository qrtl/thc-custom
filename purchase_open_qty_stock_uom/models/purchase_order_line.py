# Copyright 2025 Quartile Limited
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    def _compute_qty_to_receive(self):
        super()._compute_qty_to_receive()
        for line in self:
            if line.product_id and line.product_id.uom_id != line.product_uom:
                line.qty_to_receive_stock_uom = line.product_uom._compute_quantity(
                    line.qty_to_receive, line.product_id.uom_id
                )
            else:
                line.qty_to_receive_stock_uom = line.qty_to_receive
        return

    qty_to_receive_stock_uom = fields.Float(
        compute="_compute_qty_to_receive",
        digits="Product Unit of Measure",
        string="Qty to Receive (Stock UoM)",
    )
