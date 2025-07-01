# Copyright 2025 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models


class StockMove(models.Model):
    _inherit = "stock.move"

    @api.model
    def _read_group(
        self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True
    ):
        if self.env.context.get("actual_date"):
            domain = [
                ("actual_date",) + condition[1:]
                if isinstance(condition, (list, tuple)) and condition[0] == "date"
                else condition
                for condition in domain
            ]
        return super()._read_group(
            domain,
            fields,
            groupby,
            offset=offset,
            limit=limit,
            orderby=orderby,
            lazy=lazy,
        )
