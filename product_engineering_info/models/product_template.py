# Copyright 2026 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import Command, _, api, fields, models
from odoo.exceptions import ValidationError


class ProductTemplate(models.Model):
    _inherit = "product.template"

    allow_purchase = fields.Boolean(
        default=True,
        help="Whether the part may still be purchased. Unlike archiving, the "
        "product stays active in Odoo (e.g. because stock still exists).",
    )
    successor_product_id = fields.Many2one(
        "product.template",
        string="Successor P/N",
        help="Part that supersedes this one.",
    )
    manufacturer_id = fields.Many2one(
        "res.partner",
        help="Actual manufacturer of the part (may differ from the vendor).",
    )
    manufacturer_pname = fields.Char(string="Manufacturer Product Name")
    manufacturer_pcode = fields.Char(string="Manufacturer Product Code")
    registered_by_id = fields.Many2one(
        "res.partner",
        string="Registered By",
        help="Person who first registered the part number.",
    )
    group_code_id = fields.Many2one(
        "product.group.code",
        string="Product Group Code",
    )
    engineering_folder_link = fields.Char(
        help="Link to the folder holding the engineering information.",
    )
    bom_link = fields.Char(
        string="BOM Link (Working)",
        help="Link to the working (editable) E-BOM.",
    )
    bom_revision = fields.Char(string="BOM Revision")
    bom_author_id = fields.Many2one(
        "res.partner",
        string="BOM Author",
    )
    bom_status = fields.Selection(
        [
            ("draft", "Draft"),
            ("in_review", "In Review"),
            ("pending_approval", "Pending Approval"),
            ("approved", "Approved"),
            ("released", "Released / Effective"),
            ("superseded", "Superseded"),
            ("obsolete", "Obsolete"),
            ("canceled", "Canceled"),
        ],
        string="BOM Status",
    )
    bom_approver_id = fields.Many2one(
        "res.partner",
        string="BOM Approver",
    )
    bom_approval_date = fields.Date(string="BOM Approval Date")
    bom_link_released = fields.Char(
        string="BOM Link (Released)",
        help="Link to the BOM of the latest released revision.",
    )
    technical_notes = fields.Text()
    compatible_product_ids = fields.Many2many(
        "product.template",
        relation="product_template_compatible_rel",
        column1="product_tmpl_id",
        column2="compatible_product_tmpl_id",
        string="Compatible P/N",
        help="Parts that may be used as substitutes when out of stock.",
    )
    legacy_number_cad = fields.Char(string="Legacy Number (CAD)")
    legacy_description_cad = fields.Char(string="Legacy Description (CAD)")

    @api.constrains("successor_product_id")
    def _check_successor_product_id(self):
        for product in self:
            if product.successor_product_id == product:
                raise ValidationError(
                    _(
                        "A product cannot be its own successor (%s).",
                        product.display_name,
                    )
                )

    @api.constrains("compatible_product_ids")
    def _check_compatible_product_ids(self):
        for product in self:
            if product in product.compatible_product_ids:
                raise ValidationError(
                    _(
                        "A product cannot be in its own compatible products (%s).",
                        product.display_name,
                    )
                )

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        # Keep the compatibility relation symmetric: if the new product lists a
        # compatible part, link it back on that part too.
        for record in records:
            targets = record.compatible_product_ids
            if targets:
                targets.with_context(skip_compatible_sync=True).write(
                    {"compatible_product_ids": [Command.link(record.id)]}
                )
        return records

    def write(self, vals):
        if self.env.context.get("skip_compatible_sync") or (
            "compatible_product_ids" not in vals
        ):
            return super().write(vals)
        # Snapshot the relation before the write so we can mirror the exact
        # additions/removals onto the other side, whatever command form is used.
        old = {rec.id: set(rec.compatible_product_ids.ids) for rec in self}
        res = super().write(vals)
        for rec in self:
            new = set(rec.compatible_product_ids.ids)
            added = new - old[rec.id] - {rec.id}
            removed = old[rec.id] - new - {rec.id}
            if added:
                self.browse(added).with_context(skip_compatible_sync=True).write(
                    {"compatible_product_ids": [Command.link(rec.id)]}
                )
            if removed:
                self.browse(removed).with_context(skip_compatible_sync=True).write(
                    {"compatible_product_ids": [Command.unlink(rec.id)]}
                )
        return res
