# Copyright 2026 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests import TransactionCase


class TestStockLotTopParent(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        stock_location = cls.env.ref("stock.stock_location_stock")
        cls.loc_a = cls.env["stock.location"].create(
            {"name": "TP Loc A", "usage": "internal", "location_id": stock_location.id}
        )
        cls.loc_b = cls.env["stock.location"].create(
            {"name": "TP Loc B", "usage": "internal", "location_id": stock_location.id}
        )
        cls.loc_customer = cls.env["stock.location"].create(
            {"name": "TP Customer", "usage": "customer"}
        )
        cls.parent_product = cls.env["product.product"].create(
            {
                "name": "Top Parent Product",
                "detailed_type": "product",
                "tracking": "lot",
            }
        )
        cls.child_product = cls.env["product.product"].create(
            {"name": "Child Product", "detailed_type": "product", "tracking": "lot"}
        )
        cls.parent_lot = cls.env["stock.lot"].create(
            {
                "name": "PARENT-0001",
                "product_id": cls.parent_product.id,
                "company_id": cls.env.company.id,
            }
        )
        cls.child_lot = cls.env["stock.lot"].create(
            {
                "name": "CHILD-0001",
                "product_id": cls.child_product.id,
                "company_id": cls.env.company.id,
            }
        )

    def _add_quant(self, lot, location, quantity):
        self.env["stock.quant"]._update_available_quantity(
            lot.product_id, location, quantity, lot_id=lot
        )

    def test_physical_location_internal_only(self):
        self._add_quant(self.parent_lot, self.loc_a, 5)
        self._add_quant(self.parent_lot, self.loc_b, 3)
        self._add_quant(self.parent_lot, self.loc_customer, 2)
        self.child_lot.top_parent_lot_id = self.parent_lot
        self.assertEqual(
            self.child_lot.top_parent_location_ids, self.loc_a | self.loc_b
        )

    def test_physical_location_no_parent_uses_self(self):
        self._add_quant(self.child_lot, self.loc_a, 4)
        self.assertFalse(self.child_lot.top_parent_lot_id)
        self.assertEqual(self.child_lot.top_parent_location_ids, self.loc_a)

    def test_no_parent_no_stock_is_empty(self):
        self.assertFalse(self.child_lot.top_parent_lot_id)
        self.assertFalse(self.child_lot.top_parent_product_id)
        self.assertFalse(self.child_lot.top_parent_location_ids)
