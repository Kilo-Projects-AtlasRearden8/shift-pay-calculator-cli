# STATUS

## What was built

`shift-pay-calculator-cli` — a local-first, offline Python CLI for healthcare workers to estimate shift pay.

Package `shift_pay/`:
- `calculator.py` — pay math: base rate, shift differential, overtime (1.5x over threshold), holiday premium (2.0x by default). Returns a structured `ShiftEstimate`.
- `storage.py` — append-only JSON log of estimates (`shift_pay_log.json` by default).
- `export.py` — CSV export of the log.
- `cli.py` — argparse CLI with `calculate`, `log`, and `export` subcommands.
- `__main__.py` — enables `python3 -m shift_pay`.

Tests (`tests/test_calculator.py`): 9 unit tests covering regular pay, overtime, holiday premiums, differentials, custom multipliers, zero hours, rounding, and serialization. All pass.

Also included: `pyproject.toml` (with `shift-pay` console script), `README.md`, `MIT LICENSE` (Copyright (c) 2026 Asdale Dynamics, LLC), `.gitignore`.

## How to run

```bash
# From the repo folder
python3 -m shift_pay calculate --rate 35 --hours 12 --holiday-hours 4 \
  --differential 3 --differential-hours 8 --note "ER night shift"

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

- `python3 -m unittest discover -s tests`: 9/9 tests OK
- `pip install .` in a clean venv: OK; `shift-pay --help` works
- `calculate` → correct math (12h, $35, 4 holiday h, $3 differential on 8h → $584.00 total)
- `log` → displays appended records
- `export` → writes CSV with all fields

## Known gaps

- Overtime threshold applies per calculation, not cumulatively across a week or multiple shifts.
- No tax, benefit, or deduction modeling.
- Simplified holiday/overtime interaction (holiday hours count toward the OT threshold).
- No validation rejecting negative hours or rates.
- No edit/delete of log entries; append-only by design.
