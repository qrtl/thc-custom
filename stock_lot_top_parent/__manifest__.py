# Copyright 2026 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Stock Lot Top Parent",
    "version": "16.0.1.0.0",
    "category": "Inventory",
    "license": "AGPL-3",
    "author": "Quartile",
    "website": "https://www.quartile.co",
    "maintainers": ["nobuQuartile"],
    "summary": "Track the top-level parent serial, part number and current "
    "physical location on lots/serials.",
    "depends": ["stock"],
    "data": [
        "views/stock_lot_views.xml",
    ],
    "installable": True,
}
