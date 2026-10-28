"""Tests for shift pay math."""

from __future__ import annotations

import unittest

from shift_pay.calculator import ShiftInputs, estimate_shift_pay


class TestShiftPay(unittest.TestCase):
    def test_regular_shift_only(self) -> None:
        estimate = estimate_shift_pay(ShiftInputs(base_rate=35.0, hours_worked=40.0))
        self.assertEqual(estimate.regular_pay, 1400.00)
        self.assertEqual(estimate.ot_hours, 0.0)
        self.assertEqual(estimate.ot_pay, 0.0)
        self.assertEqual(estimate.holiday_pay, 0.0)
        self.assertEqual(estimate.total_pay, 1400.00)

    def test_overtime_pay(self) -> None:
        estimate = estimate_shift_pay(ShiftInputs(base_rate=35.0, hours_worked=45.0))
        self.assertEqual(estimate.regular_pay, 1400.00)
        self.assertEqual(estimate.ot_hours, 5.0)
        self.assertEqual(estimate.ot_pay, 262.50)
        self.assertEqual(estimate.total_pay, 1662.50)

    def test_holiday_hours_paid_at_multiplier(self) -> None:
        estimate = estimate_shift_pay(
            ShiftInputs(base_rate=35.0, hours_worked=12.0, holiday_hours=8.0)
        )
        self.assertEqual(estimate.holiday_pay, 560.00)
        self.assertEqual(estimate.regular_pay, 140.00)
        self.assertEqual(estimate.total_pay, 700.00)

    def test_holiday_hours_count_toward_ot_threshold(self) -> None:
        estimate = estimate_shift_pay(
            ShiftInputs(
                base_rate=40.0,
                hours_worked=45.0,
                holiday_hours=10.0,
            )
        )
        self.assertEqual(estimate.holiday_pay, 800.00)
        self.assertEqual(estimate.ot_hours, 5.0)
        self.assertEqual(estimate.ot_pay, 300.00)

    def test_shift_differential(self) -> None:
        estimate = estimate_shift_pay(
            ShiftInputs(base_rate=35.0, hours_worked=12.0, differential_rate=4.50, differential_hours=12.0)
        )
        self.assertEqual(estimate.differential_pay, 54.00)
        self.assertEqual(estimate.total_pay, 474.00)

    def test_custom_ot_and_holiday_multipliers(self) -> None:
        estimate = estimate_shift_pay(
            ShiftInputs(
                base_rate=30.0,
                hours_worked=42.0,
                holiday_hours=6.0,
                holiday_multiplier=2.5,
                ot_threshold=36.0,
                ot_multiplier=2.0,
            )
        )
        self.assertEqual(estimate.holiday_pay, 450.00)
        self.assertEqual(estimate.ot_hours, 6.0)
        self.assertEqual(estimate.ot_pay, 360.00)
        self.assertEqual(estimate.regular_pay, 1080.00)
        self.assertEqual(estimate.total_pay, 1890.00)

    def test_zero_hours(self) -> None:
        estimate = estimate_shift_pay(ShiftInputs(base_rate=35.0, hours_worked=0.0))
        self.assertEqual(estimate.total_pay, 0.00)

    def test_rounding(self) -> None:
        estimate = estimate_shift_pay(ShiftInputs(base_rate=33.33, hours_worked=7.5))
        self.assertEqual(estimate.total_pay, 249.97)

    def test_as_dict_contains_total(self) -> None:
        estimate = estimate_shift_pay(ShiftInputs(base_rate=20.0, hours_worked=5.0))
        data = estimate.as_dict()
        self.assertEqual(data["total_pay"], 100.00)
        self.assertEqual(data["base_rate"], 20.0)


if __name__ == "__main__":
    unittest.main()
