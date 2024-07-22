# Copyright 2024 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from dateutil.relativedelta import relativedelta

from odoo import api, fields, models


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    price_subtotal_billed = fields.Monetary(
        compute="_compute_price_subtotal_billed", store=True
    )
    price_subtotal_unbilled = fields.Monetary(
        compute="_compute_price_subtotal_billed", store=True
    )
    payment_term_id = fields.Many2one(related="order_id.payment_term_id", store=True)
    expected_payment_date = fields.Date(
        compute="_compute_expected_payment_date", store=True
    )

    @api.depends("price_unit", "qty_invoiced", "qty_to_invoice")
    def _compute_price_subtotal_billed(self):
        for line in self:
            if line.is_deposit:
                line.price_subtotal_billed = 0.0
                line.price_subtotal_unbilled = (
                    sum(
                        line.invoice_lines.filtered(
                            lambda l: l.move_id.state != "cancel"
                        ).mapped("balance")
                    )
                    * -1
                )
                continue
            line.price_subtotal_billed = line.price_unit * line.qty_invoiced
            line.price_subtotal_unbilled = line.price_unit * line.qty_to_invoice

    @api.depends("date_planned", "payment_term_id")
    def _compute_expected_payment_date(self):
        for line in self:
            if line.date_planned and line.payment_term_id:
                date = fields.Date.context_today(self, line.date_planned)
                payment_term_line = line.payment_term_id.line_ids[0]
                date += relativedelta(
                    months=payment_term_line.months, days=payment_term_line.days
                )
                if payment_term_line.end_month:
                    start_next_month = date + relativedelta(day=1, months=1)
                    date = start_next_month - relativedelta(days=1)
                date += relativedelta(days=payment_term_line.days_after)
                line.expected_payment_date = date
            else:
                line.expected_payment_date = False
