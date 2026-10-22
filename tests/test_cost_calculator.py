import importlib.util
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "cost_calculator.py"
SPEC = importlib.util.spec_from_file_location("cost_calculator", SCRIPT)
cost_calculator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(cost_calculator)


class CostCalculatorTests(unittest.TestCase):
    def test_one_time_total(self):
        self.assertEqual(cost_calculator.calculate({"one_time": [{"amount": "29.90"}]})["known_total"], "29.90")

    def test_quantity_is_explicitly_pre_multiplied_by_caller(self):
        self.assertEqual(cost_calculator.calculate({"one_time": [{"amount": "60"}, {"amount": "60"}]})["known_total"], "120.00")

    def test_recurring_periods(self):
        result = cost_calculator.calculate({"recurring": [{"amount_per_period": "18", "periods": 12}]})
        self.assertEqual(result["known_total"], "216.00")

    def test_installments(self):
        result = cost_calculator.calculate({"installments": [{"amount_per_period": "333.33", "periods": 3}]})
        self.assertEqual(result["known_total"], "999.99")

    def test_extra_fee_added(self):
        result = cost_calculator.calculate({"one_time": [{"amount": "100"}], "fees": [{"amount": "12.50"}]})
        self.assertEqual(result["known_total"], "112.50")

    def test_discount_comparison_does_not_change_total(self):
        result = cost_calculator.calculate({"one_time": [{"amount": "80"}], "offer_comparisons": [{"reference_amount": "100", "offer_amount": "80"}]})
        self.assertEqual(result["known_total"], "80.00")
        self.assertEqual(result["offer_comparisons"][0]["difference"], "20.00")

    def test_unknown_cost_prevents_complete_total_claim(self):
        result = cost_calculator.calculate({"one_time": [{"amount": "80"}], "unknown_costs": ["退租清洁费"]})
        self.assertFalse(result["total_is_complete"])
        self.assertEqual(result["known_total"], "80.00")

    def test_empty_amounts_total_zero(self):
        result = cost_calculator.calculate({})
        self.assertEqual(result["known_total"], "0.00")
        self.assertFalse(result["total_is_complete"])

    def test_decimal_is_exact(self):
        result = cost_calculator.calculate({"one_time": [{"amount": "0.10"}, {"amount": "0.20"}]})
        self.assertEqual(result["known_total"], "0.30")

    def test_more_than_two_decimal_places_are_not_rounded(self):
        result = cost_calculator.calculate({"one_time": [{"amount": "1.005"}]})
        self.assertEqual(result["known_total"], "1.005")
        self.assertEqual(result["breakdown"][0]["amount"], "1.005")

    def test_precision_is_preserved_after_multiplication(self):
        result = cost_calculator.calculate({"installments": [{"amount_per_period": "0.335", "periods": 3}]})
        self.assertEqual(result["known_total"], "1.005")

    def test_negative_amount_rejected(self):
        with self.assertRaises(cost_calculator.InputError):
            cost_calculator.calculate({"one_time": [{"amount": "-1"}]})

    def test_missing_amount_rejected(self):
        with self.assertRaises(cost_calculator.InputError):
            cost_calculator.calculate({"one_time": [{"label": "漏填"}]})

    def test_zero_periods_rejected(self):
        with self.assertRaises(cost_calculator.InputError):
            cost_calculator.calculate({"recurring": [{"amount_per_period": "10", "periods": 0}]})

    def test_binary_float_rejected(self):
        with self.assertRaises(cost_calculator.InputError):
            cost_calculator.calculate({"one_time": [{"amount": 0.1}]})

    def test_unknowns_must_be_a_list(self):
        with self.assertRaises(cost_calculator.InputError):
            cost_calculator.calculate({"unknown_costs": "不知道"})


if __name__ == "__main__":
    unittest.main()
