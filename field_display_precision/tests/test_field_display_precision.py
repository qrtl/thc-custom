# Copyright 2025 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo_test_helper import FakeModelLoader

from odoo.tests import common, tagged


@tagged("post_install", "-at_install")
class TestFieldDisplayPrecision(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.loader = FakeModelLoader(cls.env, cls.__module__)
        cls.loader.backup_registry()
        from .test_models import TestFieldDisplayPrecisionModel

        cls.loader.update_registry((TestFieldDisplayPrecisionModel,))
        test_model = cls.env.ref(
            "field_display_precision.model_test_field_display_precision"
        )
        price_unit_field = cls.env["ir.model.fields"]._get(
            "test.field.display.precision", "price_unit"
        )
        cls.second_company = cls.env["res.company"].create({"name": "Second Company"})
        cls.field_display_precision_rec = cls.env["field.display.precision"].create(
            {
                "model_id": test_model.id,
                "field_id": price_unit_field.id,
                "digits": 3,
            }
        )
        cls.field_display_precision_rec_company = cls.env[
            "field.display.precision"
        ].create(
            {
                "model_id": test_model.id,
                "field_id": price_unit_field.id,
                "digits": 4,
                "company_id": cls.second_company.id,
            }
        )
        cls.test_record = cls.env["test.field.display.precision"].create(
            {
                "name": "Test",
                "price_unit": 1.555,
            }
        )

    @classmethod
    def tearDownClass(cls):
        cls.loader.restore_registry()
        return super().tearDownClass()

    def test_field_display_precision(self):
        field_info = self.env["test.field.display.precision"].fields_get(["price_unit"])
        digits = field_info["price_unit"]["digits"][1]
        self.assertEqual(digits, 3)

    def test_field_display_precision_second_company(self):
        self.env.company = self.second_company
        field_info = self.env["test.field.display.precision"].fields_get(["price_unit"])
        digits = field_info["price_unit"]["digits"][1]
        self.assertEqual(digits, 4)

    def test_field_display_precision_standard(self):
        self.field_display_precision_rec.unlink()
        field_info = self.env["test.field.display.precision"].fields_get(["price_unit"])
        digits = field_info["price_unit"]["digits"][1]
        self.assertEqual(digits, 2)  # fallback from "Product Price"
