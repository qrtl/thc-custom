# Copyright 2024 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class StockValuationLayer(models.Model):
    _inherit = "stock.valuation.layer"

    related_valuation_layer_ids = fields.Many2many(
        "stock.valuation.layer",
        "Related Valuation Layers (incl. self)",
        compute="_compute_related_valuation_layer_ids",
    )

    def _compute_related_valuation_layer_ids(self):
        for rec in self:
            origin_svl = rec
            if not origin_svl.stock_move_id:
                origin_svl = rec.stock_valuation_layer_id
            rec.related_valuation_layer_ids = (
                origin_svl.stock_valuation_layer_ids | origin_svl
            )
