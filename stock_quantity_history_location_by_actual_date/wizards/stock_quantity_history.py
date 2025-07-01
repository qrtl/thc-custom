# Copyright 2025 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models
from odoo.tools.safe_eval import safe_eval


class StockQuantityHistory(models.TransientModel):
    _inherit = "stock.quantity.history"

    def open_at_actual_date_location(self):
        action = self.open_at_date()
        ctx = action["context"]
        ctx = safe_eval(ctx) if isinstance(ctx, str) else ctx
        ctx["actual_date"] = True
        return action
