"""Shift pay estimation for healthcare workers (education only, not a pay stub)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ShiftInputs:
    """Inputs for a single shift pay estimate."""

    base_rate: float
    hours_worked: float
    holiday_hours: float = 0.0
    holiday_multiplier: float = 2.0
    ot_threshold: float = 40.0
    ot_multiplier: float = 1.5
    differential_rate: float = 0.0
    differential_hours: float = 0.0
    weekly_hours_so_far: float = 0.0


@dataclass
class ShiftEstimate:
    """Result of a shift pay estimate."""

    base_rate: float
    hours_worked: float
    holiday_hours: float
    holiday_multiplier: float
    ot_threshold: float
    ot_multiplier: float
    differential_rate: float
    differential_hours: float
    weekly_hours_so_far: float
    holiday_pay: float
    regular_pay: float
    ot_hours: float
    ot_pay: float
    differential_pay: float
    total_pay: float

    def as_dict(self) -> dict:
        return {
            "base_rate": self.base_rate,
            "hours_worked": self.hours_worked,
            "holiday_hours": self.holiday_hours,
            "holiday_multiplier": self.holiday_multiplier,
            "ot_threshold": self.ot_threshold,
            "ot_multiplier": self.ot_multiplier,
            "differential_rate": self.differential_rate,
            "differential_hours": self.differential_hours,
            "weekly_hours_so_far": self.weekly_hours_so_far,
            "holiday_pay": self.holiday_pay,
            "regular_pay": self.regular_pay,
            "ot_hours": self.ot_hours,
            "ot_pay": self.ot_pay,
            "differential_pay": self.differential_pay,
            "total_pay": self.total_pay,
        }


def estimate_shift_pay(inputs: ShiftInputs) -> ShiftEstimate:
    """Estimate gross pay for one shift.

    Rules (education-only simplified model):
      * Holiday hours are paid at base_rate * holiday_multiplier.
      * Non-holiday hours up to the weekly OT threshold are paid at base_rate.
      * Non-holiday hours past the weekly OT threshold are paid at
        base_rate * ot_multiplier.
      * Shift differential is a flat extra amount per differential hour.
      * weekly_hours_so_far counts hours already worked this week so OT
        accumulates across multiple shifts.
    """

    base_rate = inputs.base_rate
    hours_worked = inputs.hours_worked
    holiday_hours = inputs.holiday_hours
    holiday_multiplier = inputs.holiday_multiplier
    ot_threshold = inputs.ot_threshold
    ot_multiplier = inputs.ot_multiplier
    differential_rate = inputs.differential_rate
    differential_hours = inputs.differential_hours
    weekly_hours_so_far = inputs.weekly_hours_so_far

    if base_rate < 0:
        raise ValueError("base_rate cannot be negative")
    if hours_worked < 0:
        raise ValueError("hours_worked cannot be negative")
    if holiday_hours < 0:
        raise ValueError("holiday_hours cannot be negative")
    if holiday_hours > hours_worked:
        raise ValueError("holiday_hours cannot exceed hours_worked")
    if holiday_multiplier < 0:
        raise ValueError("holiday_multiplier cannot be negative")
    if ot_threshold < 0:
        raise ValueError("ot_threshold cannot be negative")
    if ot_multiplier < 0:
        raise ValueError("ot_multiplier cannot be negative")
    if differential_rate < 0:
        raise ValueError("differential_rate cannot be negative")
    if differential_hours < 0:
        raise ValueError("differential_hours cannot be negative")
    if weekly_hours_so_far < 0:
        raise ValueError("weekly_hours_so_far cannot be negative")

    holiday_pay = round(holiday_hours * base_rate * holiday_multiplier, 2)
    non_holiday_hours = hours_worked - holiday_hours
    remaining_regular_hours = max(0.0, ot_threshold - weekly_hours_so_far)
    regular_hours = max(0.0, min(non_holiday_hours, remaining_regular_hours))
    ot_hours = max(0.0, non_holiday_hours - remaining_regular_hours)
    regular_pay = round(regular_hours * base_rate, 2)
    ot_pay = round(ot_hours * base_rate * ot_multiplier, 2)
    differential_pay = round(differential_hours * differential_rate, 2)
    total_pay = round(holiday_pay + regular_pay + ot_pay + differential_pay, 2)

    return ShiftEstimate(
        base_rate=base_rate,
        hours_worked=hours_worked,
        holiday_hours=holiday_hours,
        holiday_multiplier=holiday_multiplier,
        ot_threshold=ot_threshold,
        ot_multiplier=ot_multiplier,
        differential_rate=differential_rate,
        differential_hours=differential_hours,
        weekly_hours_so_far=weekly_hours_so_far,
        holiday_pay=holiday_pay,
        regular_pay=regular_pay,
        ot_hours=ot_hours,
        ot_pay=ot_pay,
        differential_pay=differential_pay,
        total_pay=total_pay,
    )
