# Copyright 2024 Quartile Limited
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, models
from odoo.exceptions import UserError


class ResPartner(models.Model):
    _inherit = "res.partner"

    def signup_prepare(self, signup_type="signup", expiration=False):
        # Signup token seems to get generated for followers with no portal access when
        # "free signup" is enabled and an unauthorized user mentions a partner (any
        # partner) in a message. We should skip the check in this case.
        self = self.with_context(skip_partner_check=True)
        return super().signup_prepare(signup_type=signup_type, expiration=expiration)

    @api.model
    def _user_is_partner_admin(self):
        return self.env.user.has_group(
            "partner_group_partner_admin.group_partner_admin"
        )

    @api.model
    def _raise_partner_error(self):
        raise UserError(
            _("You are not allowed to create/edit a partner with no parent.")
        )

    @api.model_create_multi
    def create(self, vals_list):
        if self._user_is_partner_admin():
            return super().create(vals_list)
        # To avoid unnecessary check in the write method called by the create method.
        self = self.with_context(skip_partner_check=True)
        res = super().create(vals_list)
        if res.filtered(lambda x: not x.parent_id):
            self._raise_partner_error()
        return res

    def write(self, vals):
        # No restriction with update of own partner.
        if self.ids == [self.env.user.partner_id.id]:
            return super().write(vals)
        if self._user_is_partner_admin() or self._context.get("skip_partner_check"):
            return super().write(vals)
        if not self.filtered(lambda x: not x.parent_id) and "parent_id" not in vals:
            return super().write(vals)
        if len(vals) > 1 or "child_ids" not in vals:
            self._raise_partner_error()
        # There can be an unwanted error when updating a child partner through the
        # parent form without this.
        self = self.with_context(skip_partner_check=True)
        return super().write(vals)
