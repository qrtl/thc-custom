# Copyright 2026 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import Command
from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestProductEngineeringInfo(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        Product = cls.env["product.template"]
        cls.product_a = Product.create({"name": "Part A"})
        cls.product_b = Product.create({"name": "Part B"})
        cls.product_c = Product.create({"name": "Part C"})

    def test_compatible_sync_on_create(self):
        product = self.env["product.template"].create(
            {
                "name": "Part D",
                "compatible_product_ids": [Command.link(self.product_a.id)],
            }
        )
        self.assertIn(product, self.product_a.compatible_product_ids)
        self.assertIn(self.product_a, product.compatible_product_ids)

    def test_compatible_sync_add_on_write_and_unlink(self):
        self.product_a.compatible_product_ids = [Command.link(self.product_b.id)]
        self.assertIn(self.product_b, self.product_a.compatible_product_ids)
        self.assertIn(self.product_a, self.product_b.compatible_product_ids)
        self.product_a.compatible_product_ids = [Command.unlink(self.product_b.id)]
        self.assertNotIn(self.product_b, self.product_a.compatible_product_ids)
        self.assertNotIn(self.product_a, self.product_b.compatible_product_ids)

    def test_compatible_sync_set_replaces_both_sides(self):
        self.product_a.compatible_product_ids = [Command.link(self.product_b.id)]
        self.product_a.compatible_product_ids = [Command.set([self.product_c.id])]
        self.assertNotIn(self.product_a, self.product_b.compatible_product_ids)
        self.assertIn(self.product_a, self.product_c.compatible_product_ids)

    def test_compatible_sync_on_unlink(self):
        self.product_a.compatible_product_ids = [Command.link(self.product_b.id)]
        self.product_a.unlink()
        self.assertFalse(self.product_b.compatible_product_ids)

    def test_compatible_self_reference_blocked(self):
        with self.assertRaises(ValidationError):
            self.product_a.compatible_product_ids = [Command.link(self.product_a.id)]

    def test_successor_self_reference_blocked(self):
        with self.assertRaises(ValidationError):
            self.product_a.successor_product_id = self.product_a
