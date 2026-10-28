"""Command-line interface for the shift pay calculator."""

from __future__ import annotations

import argparse
import sys
from typing import Optional, Sequence

from shift_pay.calculator import ShiftInputs, estimate_shift_pay
from shift_pay.export import export_csv
from shift_pay.storage import ShiftLog

DISCLAIMER = (
    "Education only. Estimates are not a pay stub, not legal or tax advice, "
    "and do not account for taxes, benefits, or local labor laws."
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="shift-pay",
        description="Estimate healthcare shift pay (education only, not a pay stub).",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    calc = subparsers.add_parser(
        "calculate", help="Estimate gross pay for one shift."
    )
    calc.add_argument("--rate", type=float, required=True, help="Base hourly rate.")
    calc.add_argument(
        "--hours", type=float, required=True, help="Total hours worked on the shift."
    )
    calc.add_argument(
        "--holiday-hours",
        type=float,
        default=0.0,
        help="Hours worked on a holiday (subset of total hours).",
    )
    calc.add_argument(
        "--holiday-multiplier",
        type=float,
        default=2.0,
        help="Pay multiplier for holiday hours (default: 2.0).",
    )
    calc.add_argument(
        "--ot-threshold",
        type=float,
        default=40.0,
        help="Weekly hours before overtime begins (default: 40).",
    )
    calc.add_argument(
        "--ot-multiplier",
        type=float,
        default=1.5,
        help="Overtime pay multiplier (default: 1.5).",
    )
    calc.add_argument(
        "--differential",
        type=float,
        default=0.0,
        help="Extra pay per hour for shift differential (default: 0).",
    )
    calc.add_argument(
        "--differential-hours",
        type=float,
        default=0.0,
        help="Hours eligible for the shift differential (default: 0).",
    )
    calc.add_argument(
        "--weekly-hours-so-far",
        type=float,
        default=0.0,
        help="Hours already worked this week before this shift (default: 0).",
    )
    calc.add_argument("--note", default="", help="Optional note saved with the log entry.")
    calc.add_argument(
        "--no-log",
        action="store_true",
        help="Do not save this estimate to the local JSON log.",
    )
    calc.add_argument(
        "--log",
        default="shift_pay_log.json",
        help="Path to the local JSON log file (default: shift_pay_log.json).",
    )

    log_cmd = subparsers.add_parser("log", help="Show the local JSON log of estimates.")
    log_cmd.add_argument(
        "--log", default="shift_pay_log.json", help="Path to the local JSON log file."
    )

    export_cmd = subparsers.add_parser(
        "export", help="Export the local JSON log to CSV."
    )
    export_cmd.add_argument(
        "--log", default="shift_pay_log.json", help="Path to the local JSON log file."
    )
    export_cmd.add_argument(
        "--output", required=True, help="Output CSV file path."
    )

    return parser


def run(argv: Optional[Sequence[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "calculate":
        try:
            inputs = ShiftInputs(
                base_rate=args.rate,
                hours_worked=args.hours,
                holiday_hours=args.holiday_hours,
                holiday_multiplier=args.holiday_multiplier,
                ot_threshold=args.ot_threshold,
                ot_multiplier=args.ot_multiplier,
                differential_rate=args.differential,
                differential_hours=args.differential_hours,
                weekly_hours_so_far=args.weekly_hours_so_far,
            )
            estimate = estimate_shift_pay(inputs)
        except ValueError as exc:
            print(f"Error: {exc}")
            return 1

        print(f"Base pay:       ${estimate.regular_pay:.2f}")
        print(f"Holiday pay:    ${estimate.holiday_pay:.2f}")
        print(f"Overtime ({estimate.ot_hours:.1f}h): ${estimate.ot_pay:.2f}")
        print(f"Differential:   ${estimate.differential_pay:.2f}")
        print(f"{'Total pay:':<16}${estimate.total_pay:.2f}")
        if estimate.weekly_hours_so_far:
            print(
                f"Weekly total:   {estimate.weekly_hours_so_far + estimate.hours_worked:.1f}h"
            )
        print()
        print(DISCLAIMER)

        if not args.no_log:
            ShiftLog(args.log).append(estimate, note=args.note)
            print(f"\nLogged to {args.log}")

        return 0

    if args.command == "log":
        records = ShiftLog(args.log).read()
        if not records:
            print("No shift estimates logged yet.")
            return 0
        for record in records:
            print(
                f"{record.get('recorded_at', '')}  "
                f"{record.get('hours_worked', 0)}h @ "
                f"${record.get('base_rate', 0):.2f}  "
                f"total ${record.get('total_pay', 0):.2f}"
            )
        return 0

    if args.command == "export":
        records = ShiftLog(args.log).read()
        export_csv(records, args.output)
        print(f"Exported {len(records)} records to {args.output}")
        return 0

    parser.print_help()
    return 1


def main() -> None:
    sys.exit(run())


if __name__ == "__main__":
    main()
