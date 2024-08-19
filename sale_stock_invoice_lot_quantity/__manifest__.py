# Copyright 2024 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Sale Stock Invoice Lot Quantity",
    "version": "16.0.1.0.0",
    "category": "Stock",
    "license": "AGPL-3",
    "author": "Quartile",
    "website": "https://www.quartile.co",
    "depends": ["sale_stock"],
    "data": [
        "security/ir.model.access.csv",
        "views/report_invoice.xml",
    ],
    "installable": True,
}
