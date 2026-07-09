# GrokCalci

A simple command-line calculator written in Python. No external dependencies.

## Requirements

- Python 3.10+

## Run

**One-shot expression:**

```bash
python calculator.py "2 + 3 * 4"
```

**Interactive mode:**

```bash
python calculator.py
```

On Windows, if `python` points to a broken install, use the Python launcher or a full path, e.g. `py -3.11 calculator.py "2 + 2"`.

Then type expressions at the `>` prompt. Use `help` for operators, `quit` to exit.

## Supported operations

| Operator | Meaning           | Example   |
|----------|-------------------|-----------|
| `+`      | Addition          | `2 + 3`   |
| `-`      | Subtraction       | `10 - 4`  |
| `*` / `×`| Multiplication    | `6 * 7`   |
| `/` / `÷`| Division          | `15 / 3`  |
| `//`     | Floor division    | `7 // 2`  |
| `%`      | Modulo            | `10 % 3`  |
| `**` / `^` | Power           | `2^8`     |
| `( )`    | Grouping          | `(2+3)*4` |

Expressions are evaluated safely (no `eval()` of arbitrary code).

## Tests

```bash
python -m unittest test_calculator.py -v
```
