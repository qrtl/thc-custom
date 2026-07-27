# Copyright 2026 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


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
    registered_by = fields.Char(help="Person who first registered the part number.")
    group_code_id = fields.Many2one(
        "product.group.code",
        string="Product Group Code",
    )
    engineering_folder_link = fields.Char(
        help="Link to the Google Drive folder holding the engineering information.",
    )
    bom_link = fields.Char(
        string="BOM Link (Working)",
        help="Link to the working (editable) E-BOM.",
    )
    bom_revision = fields.Char(string="BOM Revision")
    bom_author = fields.Char(string="BOM Author")
    bom_status = fields.Char(string="BOM Status")
    bom_approver = fields.Char(string="BOM Approver")
    bom_approval_date = fields.Char(string="BOM Approval Date")
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
