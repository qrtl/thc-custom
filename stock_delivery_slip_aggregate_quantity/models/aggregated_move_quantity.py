# Copyright 2024 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class AggregatedMoveQuantity(models.TransientModel):
    _name = "aggregated.move.quantity"
    _description = "Aggregated Move Quantity"

    product_id = fields.Many2one("product.product")
    qty_ordered = fields.Float(digits="Product Unit of Measure")
    qty_done = fields.Float(digits="Product Unit of Measure")
