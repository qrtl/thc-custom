# Copyright 2024 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Purchase Order Line Payment Forecast",
    "version": "16.0.1.0.0",
    "category": "Purchases",
    "license": "AGPL-3",
    "author": "Quartile",
    "website": "https://www.quartile.co",
    "depends": ["purchase_deposit", "purchase_order_line_menu"],
    "data": [
        "views/purchase_order_views.xml",
        "views/purchase_order_line_views.xml",
    ],
    "pre_init_hook": "pre_init_hook",
    "installable": True,
}
