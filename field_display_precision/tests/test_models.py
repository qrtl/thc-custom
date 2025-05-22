# Copyright 2025 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class TestFieldDisplayPrecisionModel(models.Model):
    _name = "test.field.display.precision"

    name = fields.Char()
    price_unit = fields.Float(string="Unit Price", digits="Product Price")
