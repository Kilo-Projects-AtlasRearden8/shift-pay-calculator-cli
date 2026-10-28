# Shift Pay Calculator CLI

A local, offline Python CLI that helps healthcare workers estimate shift pay:
base hourly rate, shift differentials, overtime, and holiday premiums. Results
are saved to a local JSON log and can be exported to CSV.

Built and maintained by **Asdale Dynamics, LLC** (Dylan Asdale, Indiana —
formed October 2026). Beginner-friendly, local-first, tested, open-source.
No cloud, no accounts, no tracking.

## Education only — not a pay stub

This tool is for education and estimation only. It is **not** a pay stub, not
legal or tax advice, and does not account for taxes, benefits, shift rules,
or local labor laws. Always confirm your actual pay with your employer or
payroll department.

## Install

```bash
git clone <this-repo>
cd shift-pay-calculator-cli
pip install .
```

Or run without installing:

```bash
python3 -m shift_pay calculate --rate 35 --hours 12
```

## Usage

Estimate one shift:

```bash
shift-pay calculate --rate 35 --hours 12 --holiday-hours 4 \
  --differential 3.00 --differential-hours 8 --note "Night shift, ER"
```

Options:

* `--rate` — base hourly rate (required)
* `--hours` — total hours worked (required)
* `--holiday-hours` — hours worked on a holiday (default: 0)
* `--holiday-multiplier` — holiday pay multiplier (default: 2.0)
* `--ot-threshold` — hours before overtime (default: 40)
* `--ot-multiplier` — overtime multiplier (default: 1.5)
* `--differential` — extra $/hour for shift differential (default: 0)
* `--differential-hours` — hours eligible for differential (default: 0)
* `--note` — optional note saved with the log entry
* `--no-log` — skip saving to the local JSON log
* `--log` — log file path (default: `shift_pay_log.json`)

Pay model (simplified, education only):

* Holiday hours: `base_rate × holiday_multiplier`
* Non-holiday hours up to the OT threshold: `base_rate`
* Hours over the OT threshold: `base_rate × ot_multiplier`
* Shift differential: flat amount per differential hour

View the local log:

```bash
shift-pay log
```

Export the log to CSV:

```bash
shift-pay export --output shifts.csv
```

## Tests

```bash
python3 -m unittest discover -s tests
```

## License

MIT License. Copyright (c) 2026 Asdale Dynamics, LLC. See `LICENSE`.

## About

Asdale Dynamics, LLC is Dylan Asdale's Indiana LLC (formed October 2026),
focused on beginner-friendly AI education, books and guides, and practical
local-first tools. Dylan is a registered nurse turned AI author; his book
_The Massive AI Manual_ and hub site dylanasdale.github.io explain AI "like a
friend would": plain English, step by step, never condescending.
