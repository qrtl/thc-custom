# Copyright 2024 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class AccountMove(models.Model):
    _inherit = "account.move"

    def _get_invoiced_lot_values(self):
        lot_values = super()._get_invoiced_lot_values()
        for lot_value in lot_values:
            qty = float(lot_value["quantity"])
            lot_quantity = self.env["lot.quantity"].create(
                {
                    "lot_id": lot_value["lot_id"],
                    "quantity": qty,
                }
            )
            lot_value["lot_quantity"] = lot_quantity
        return lot_values
