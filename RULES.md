# Notebook Rules

## Source of truth

Build scripts generate notebooks. Do not edit `.ipynb` files directly.

```
# One topic:
uv run python src/ai_concepts/notebooks/build_01_tokens.py
# Output: src/ai_concepts/notebooks/01_tokens.ipynb + 01_tokens.html

# All topics (or a subset by number):
uv run python src/ai_concepts/notebooks/build_all.py
uv run python src/ai_concepts/notebooks/build_all.py 07 12
```

Shared helpers (`md()`, `code()`, `build()`) live in `src/ai_concepts/notebooks/_nb.py`.

---

## Cell string quoting rule

All cell source strings use Python string concatenation — **no triple-quoted f-strings inside cells**.

```python
# CORRECT
cells.append(code(
    "SELECT COUNT(*) FROM read_parquet('" + str(path) + "')\n"
))

# WRONG — triple-quote f-string conflicts with the outer delimiters
cells.append(code(f"""SELECT COUNT(*) FROM read_parquet('{path}')"""))
```

---

## Logging rule

Every Python script must have verbose logging throughout — not just at start/end. Log at each major step:
- counts and shapes after every load, join, filter, and feature build
- null rates for key rolling features
- leakage check result
- credit usage after every API call block

Use `logging.FileHandler` so logs persist. Always include the date in `datefmt` so entries
are unambiguous across runs. Pattern:
```python
LOG_DIR = PROJECT_ROOT / "src/ai_concepts/logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-7s  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(LOG_DIR / "stepNx_name.log", mode="w", encoding="utf-8"),
    ],
)
```

No silent functions. If a function does meaningful work, it logs what it did.
Log progress every N iterations for any loop over files or rows (e.g. every 25 files).
