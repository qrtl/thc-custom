# Copyright 2025 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class FieldDisplayPrecision(models.Model):
    _name = "field.display.precision"
    _description = "Field Display Precision"
    _order = "model_id, field_id"

    model_id = fields.Many2one("ir.model", ondelete="cascade", required=True)
    model_name = fields.Char(related="model_id.model", store=True)
    field_id = fields.Many2one(
        "ir.model.fields",
        domain="[('model_id', '=', model_id), ('ttype', '=', 'float')]",
        string="Field",
        ondelete="cascade",
        required=True,
    )
    field_name = fields.Char("Field Name", related="field_id.name", store=True)
    digits = fields.Integer()
    company_id = fields.Many2one("res.company", string="Company")
