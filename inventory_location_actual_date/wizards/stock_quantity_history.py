# Copyright 2025 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, models
from odoo.osv import expression
from odoo.tools.misc import format_datetime


class StockQuantityHistory(models.TransientModel):
    _inherit = "stock.quantity.history"

    def open_at_actual_date_location(self):
        tree_view_id = self.env.ref("stock.view_stock_product_tree").id
        form_view_id = self.env.ref("stock.product_form_view_procurement_button").id
        domain = [("type", "=", "product")]
        product_id = self.env.context.get("product_id", False)
        product_tmpl_id = self.env.context.get("product_tmpl_id", False)
        if product_id:
            domain = expression.AND([domain, [("id", "=", product_id)]])
        elif product_tmpl_id:
            domain = expression.AND(
                [domain, [("product_tmpl_id", "=", product_tmpl_id)]]
            )
        action = {
            "type": "ir.actions.act_window",
            "views": [(tree_view_id, "tree"), (form_view_id, "form")],
            "view_mode": "tree,form",
            "name": _("Products"),
            "res_model": "product.product",
            "domain": domain,
            "context": dict(
                self.env.context, to_date=self.inventory_datetime, actual_date=True
            ),
            "display_name": format_datetime(self.env, self.inventory_datetime),
        }
        return action
