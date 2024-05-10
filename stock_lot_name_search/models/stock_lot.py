# Copyright 2024 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models
from odoo.osv import expression


class StockLot(models.Model):
    _inherit = "stock.lot"

    @api.model
    def _name_search(
        self, name="", args=None, operator="ilike", limit=100, name_get_uid=None
    ):
        args = args or []
        if " " in name:  # i.e., lot name and product name are provided
            lot_name, product_name = name.split(" ", 1)
            products = self.env["product.product"].search(
                [
                    "|",
                    ("name", operator, product_name),
                    ("default_code", operator, product_name),
                ]
            )
            lot_args = [("product_id", "in", products.ids)]
            args = expression.AND([lot_args, args])
            name = lot_name
        return super()._name_search(name, args, operator, limit, name_get_uid)
