# Copyright 2024 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    def _get_aggregated_product_quantities(self, **kwargs):
        aggregated_move_lines = super()._get_aggregated_product_quantities(**kwargs)
        for _, line in aggregated_move_lines.items():
            aggregated_move_quantity = self.env["aggregated.move.quantity"].create(
                {
                    "product_id": line["product"].id,
                    "qty_ordered": line["qty_ordered"] or 0.0,
                    "qty_done": line["qty_done"] or 0.0,
                }
            )
            line["aggregated_move_quantity"] = aggregated_move_quantity
        return aggregated_move_lines
