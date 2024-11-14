# Copyright 2024 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tools.sql import column_exists


def pre_init_hook(cr):
    if not column_exists(cr, "purchase_order_line", "payment_term_id"):
        cr.execute(
            """
            ALTER TABLE purchase_order_line
            ADD COLUMN payment_term_id integer;
            UPDATE purchase_order_line pol
            SET payment_term_id = po.payment_term_id
            FROM purchase_order po
            WHERE po.id = pol.order_id;
            """
        )
