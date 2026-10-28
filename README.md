# Shift Pay Calculator CLI

A friendly, local-first Python CLI that helps healthcare workers estimate shift
pay — hourly rate, shift differentials, overtime, and holiday premiums. Results
are saved to a local JSON log and can be exported to CSV. No cloud, no accounts,
no tracking. Everything stays on your machine.

Built by **Asdale Dynamics, LLC** (Dylan Asdale, Indiana — formed October 2026).
Beginner-friendly, tested, open-source.

---

## Education only — not a pay stub

This tool is for education and estimation only. It is **not** a pay stub, not
legal or tax advice, and does not account for taxes, benefits, shift rules, or
local labor laws. Always confirm your actual pay with your employer or payroll
department before making any decisions.

---

## Install

```bash
git clone <this-repo>
cd shift-pay-calculator-cli
pip install .
```

Or run without installing:

```bash
python3 -m shift_pay calculate --rate 35 --hours 8
```

---

## How to use it

### Estimate one shift

```bash
shift-pay calculate --rate 35 --hours 12
```

That prints a pay breakdown:

```
Base pay:       $420.00
Holiday pay:    $0.00
Overtime (0.0h): $0.00
Differential:   $0.00
Total pay:      $420.00

Education only. Estimates are not a pay stub, not legal or tax advice, and do not account for taxes, benefits, or local labor laws.

Logged to shift_pay_log.json
```

### Common options

| Option | What it does | Default |
|--------|--------------|---------|
| `--rate` | Base hourly rate (required) | — |
| `--hours` | Total hours worked on the shift (required) | — |
| `--holiday-hours` | Hours worked on a holiday (part of total hours) | 0 |
| `--holiday-multiplier` | Pay multiplier for holiday hours | 2.0 |
| `--ot-threshold` | Weekly hours before overtime begins | 40 |
| `--ot-multiplier` | Overtime pay multiplier | 1.5 |
| `--differential` | Extra pay per hour for shift differential | 0 |
| `--differential-hours` | Hours eligible for the shift differential | 0 |
| `--weekly-hours-so-far` | Hours already worked this week before this shift | 0 |
| `--note` | Optional note saved with the log entry | — |
| `--no-log` | Skip saving to the local JSON log | off |
| `--log` | Log file path | shift_pay_log.json |

### Example: holiday shift with overtime and a night differential

You worked a 12-hour shift, 4 of those hours were on a holiday, you've already
worked 36 hours this week, and you get a $3.00 night differential on all 12
hours:

```bash
shift-pay calculate \
  --rate 35 \
  --hours 12 \
  --holiday-hours 4 \
  --weekly-hours-so-far 36 \
  --differential 3.00 \
  --differential-hours 12 \
  --note "Holiday night shift, ER"
```

### View your log

```bash
shift-pay log
```

### Export your log to CSV

```bash
shift-pay export --output shifts.csv
```

---

## How the pay math works (simplified, education only)

* **Holiday hours:** `base_rate × holiday_multiplier` (default 2.0×)
* **Regular hours:** non-holiday hours up to your weekly OT threshold, paid at
  `base_rate`
* **Overtime hours:** non-holiday hours past the weekly OT threshold, paid at
  `base_rate × ot_multiplier` (default 1.5×)
* **Shift differential:** a flat extra amount per differential hour

`--weekly-hours-so-far` lets overtime accumulate across multiple shifts in a
week, so your second or third shift correctly picks up overtime hours.

---

## Tests

```bash
python3 -m unittest discover -s tests
```

---

## License

MIT License. Copyright (c) 2026 Asdale Dynamics, LLC. See `LICENSE`.

---

## About

Asdale Dynamics, LLC is Dylan Asdale's Indiana LLC (formed October 2026),
focused on beginner-friendly AI education, books and guides, and practical
local-first tools. Dylan is a registered nurse turned AI author; his book
_The Massive AI Manual_ and hub site dylanasdale.github.io explain AI "like a
friend would": plain English, step by step, never condescending.
