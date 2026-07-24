# Copyright 2026 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class StockLot(models.Model):
    _inherit = "stock.lot"

    top_parent_lot_id = fields.Many2one(
        "stock.lot",
        string="Top lv Parent S/N",
        help="Serial number of the top-level parent assembly this lot belongs to.",
    )
    top_parent_product_id = fields.Many2one(
        "product.product",
        related="top_parent_lot_id.product_id",
        string="Top lv Parent P/N",
    )
    top_parent_location_ids = fields.Many2many(
        "stock.location",
        string="Physical Location",
        compute="_compute_top_parent_location_ids",
        help="Current internal locations of Top lv Parent S/N, or of this lot "
        "itself when it has no parent. Empty when it is not stored in any "
        "internal location.",
    )

    @api.depends("top_parent_lot_id")
    def _compute_top_parent_location_ids(self):
        quant_model = self.env["stock.quant"]
        for lot in self:
            target_lot = lot.top_parent_lot_id or lot
            if not target_lot.id:
                lot.top_parent_location_ids = False
                continue
            quants = quant_model.search(
                [
                    ("lot_id", "=", target_lot.id),
                    ("location_id.usage", "=", "internal"),
                    ("quantity", ">", 0),
                ]
            )
            lot.top_parent_location_ids = quants.location_id
