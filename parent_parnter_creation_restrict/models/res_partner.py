# Copyright 2024 Quartile Limited
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, models
from odoo.exceptions import UserError


class ResPartner(models.Model):
    _inherit = "res.partner"

    def _check_partner_restriction(self):
        # In case of an empty recordset or just adding child partner, check is skipped
        if not self or self.env.context.get("adding_child_partner"):
            return
        authorized_group_ids = [
            self.env.ref("base.group_system").id,
            self.env.ref("sales_team.group_sale_manager").id,
            self.env.ref("purchase.group_purchase_manager").id,
            self.env.ref("account.group_account_manager").id,
        ]
        if (
            not set(self.env.user.groups_id.ids).intersection(authorized_group_ids)
            and not self.parent_id
        ):
            raise UserError(
                _("You are not allowed to create/edit a partner with no parent.")
            )

    @api.model_create_multi
    def create(self, vals_list):
        partners = super(ResPartner, self).create(vals_list)
        for partner in partners:
            partner._check_partner_restriction()
        return partners

    def write(self, vals):
        if len(vals) == 1 and "child_ids" in vals:
            self = self.with_context(adding_child_partner=True)
        res = super(ResPartner, self).write(vals)
        self._check_partner_restriction()
        return res
