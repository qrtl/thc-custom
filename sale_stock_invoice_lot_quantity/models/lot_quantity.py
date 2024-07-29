# Copyright 2024 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class LotQuantity(models.TransientModel):
    _name = "lot.quantity"
    _description = "Lot Quantity"

    lot_id = fields.Many2one("stock.lot")
    quantity = fields.Float(digits="Product Unit of Measure")
