# Copyright 2024 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


from odoo import api, fields, models
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DF


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    company_currency_id = fields.Many2one(
        "res.currency",
        related="company_id.currency_id",
        string="Company Currency",
        readonly=True,
        store=True,
    )
    currency_rate = fields.Float(related="order_id.currency_rate")
    price_subtotal_billed = fields.Monetary(
        "Billed Amount", compute="_compute_price_subtotal_billed", store=True
    )
    price_subtotal_unbilled = fields.Monetary(
        "Unbilled Amount", compute="_compute_price_subtotal_billed", store=True
    )
    price_subtotal_unbilled_curr = fields.Monetary(
        "Unbilled Amount (Comp. Curr.)",
        compute="_compute_price_subtotal_unbilled_curr",
        currency_field="company_currency_id",
        store=True,
    )
    payment_term_id = fields.Many2one(related="order_id.payment_term_id", store=True)
    expected_payment_date = fields.Date(
        compute="_compute_expected_payment_date", store=True
    )

    @api.depends("price_unit", "qty_invoiced", "qty_to_invoice")
    def _compute_price_subtotal_billed(self):
        for line in self:
            if line.is_deposit:
                line.price_subtotal_billed = sum(
                    line.invoice_lines.filtered(
                        lambda l: l.move_id.state != "cancel"
                    ).mapped("balance")
                )
                line.price_subtotal_unbilled = line.price_subtotal_billed * -1
                continue
            line.price_subtotal_billed = line.price_unit * line.qty_invoiced
            line.price_subtotal_unbilled = line.price_unit * (
                line.product_qty - line.qty_invoiced
            )

    @api.depends("price_subtotal_unbilled", "currency_rate")
    def _compute_price_subtotal_unbilled_curr(self):
        for line in self:
            if line.currency_id.id == line.company_id.currency_id.id:
                unbilled_amount_curr = line.price_subtotal_unbilled
            else:
                unbilled_amount_curr = line.price_subtotal_unbilled / line.currency_rate
            line.price_subtotal_unbilled_curr = unbilled_amount_curr

    @api.depends("date_planned", "payment_term_id")
    def _compute_expected_payment_date(self):
        for line in self:
            if line.display_type is not False or not line.payment_term_id:
                line.expected_payment_date = False
                continue
            date_planned = fields.Date.context_today(self, line.date_planned)
            ref_date = date_planned.strftime(DF)
            pay_date = False
            # We pick the earliest payment date if the term proposes multiple dates.
            for term_line in line.payment_term_id.line_ids:
                due_date = term_line._get_due_date(ref_date)
                pay_date = due_date if not pay_date else min(pay_date, due_date)
            line.expected_payment_date = pay_date
