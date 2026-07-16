# Copyright 2026 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductGroupCode(models.Model):
    _name = "product.group.code"
    _description = "Product Group Code"
    _order = "name"

    name = fields.Char(required=True)
    active = fields.Boolean(default=True)

    _sql_constraints = [
        ("name_uniq", "unique(name)", "The Product Group Code must be unique."),
    ]
