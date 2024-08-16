# Copyright 2024 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models
from odoo.tools import float_utils


class LotQuantity(models.TransientModel):
    _name = "lot.quantity"
    _description = "Lot Quantity"

    lot_id = fields.Many2one("stock.lot")
    quantity = fields.Float(digits="Product Unit of Measure")

    def _format_quantity(self):
        self.ensure_one()
        dp_qweb_rec = self.env["decimal.precision.qweb"].search(
            [("res_model_name", "=", self._name), ("field_name", "=", "quantity")],
            limit=1,
        )
        if not dp_qweb_rec:
            precision = self.env["decimal.precision"].precision_get(
                "Product Unit of Measure"
            )
        else:
            precision = dp_qweb_rec.digits
        # Use float_utils.float_round for rounding
        rounded_value = float_utils.float_round(
            self.quantity, precision_digits=precision
        )
        # Format the rounded value as a string with the specified precision
        fmt = f"%.{precision}f"
        return fmt % rounded_value
