# Copyright 2026 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Product Engineering Info",
    "summary": "Add an Engineering tab with engineering fields and a "
    "Product Group Code classification to products.",
    "version": "16.0.1.0.0",
    "category": "Inventory",
    "license": "AGPL-3",
    "author": "Quartile",
    "website": "https://www.quartile.co",
    "maintainers": ["nobuQuartile"],
    "depends": ["purchase", "stock"],
    "data": [
        "security/ir.model.access.csv",
        "views/product_group_code_views.xml",
        "views/product_template_views.xml",
    ],
    "installable": True,
}
