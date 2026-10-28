# STATUS

## What was built

`shift-pay-calculator-cli` — a local-first, offline Python CLI for healthcare workers to estimate shift pay.

Package `shift_pay/`:
- `calculator.py` — pay math: base rate, shift differential, overtime (1.5x over weekly threshold), holiday premium (2.0x by default), weekly-hours accumulation so OT carries across multiple shifts. Input validation rejects negative values. Returns a structured `ShiftEstimate`.
- `storage.py` — append-only JSON log of estimates (`shift_pay_log.json` by default).
- `export.py` — CSV export of the log.
- `cli.py` — argparse CLI with `calculate`, `log`, and `export` subcommands. Friendly error messages for invalid input.
- `__main__.py` — enables `python3 -m shift_pay`.

Tests (`tests/test_calculator.py`): 16 unit tests covering regular pay, overtime, holiday premiums, differentials, custom multipliers, weekly-hours accumulation, zero hours, rounding, serialization, and input validation. All pass.

Also included: `pyproject.toml` (with `shift-pay` console script), `README.md`, `MIT LICENSE` (Copyright (c) 2026 Asdale Dynamics, LLC), `.gitignore`.

## How to run

```bash
# From the repo folder
python3 -m shift_pay calculate --rate 35 --hours 12 --holiday-hours 4 \
  --weekly-hours-so-far 36 --differential 3 --differential-hours 12 \
  --note "Holiday night shift, ER"

# View the local JSON log
python3 -m shift_pay log

# Export to CSV
python3 -m shift_pay export --output shifts.csv

# Or install and use the `shift-pay` command
pip install .
shift-pay calculate --rate 35 --hours 8

# Tests
python3 -m unittest discover -s tests
```

Education-only disclaimer: estimates are not a pay stub and not legal/tax advice.

## Verification results

- `python3 -m unittest discover -s tests`: 16/16 tests OK
- `pip install .` in a clean venv: OK; `shift-pay --help` and `shift-pay calculate` work
- `calculate` → correct math with holiday, weekly accumulation, and differential ($666.00 for the worked example)
- `calculate --rate -10` → friendly error, exit code 1
- `log` → displays appended records
- `export` → writes CSV with all fields including `weekly_hours_so_far`

## Known gaps

- Overtime threshold is weekly-cumulative via `--weekly-hours-so-far`, but the tool does not persist a running weekly total across log entries (user must track it manually).
- No tax, benefit, or deduction modeling.
- Holiday hours are paid at the premium rate and do not draw down the OT threshold.
- No validation rejecting differential hours exceeding hours worked.
- No edit/delete of log entries; append-only by design.
