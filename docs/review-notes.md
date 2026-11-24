# Code Review Notes: Olist Ingestion (Bronze)

**Review date:** 2026-11-24
**Scope:** `ingest_order_items()` first-pass ingestion script
**Initial rating:** 6.5/10 (solid first pass, design issues rather than syntax issues)

## What's already good
- Logging to both file and console, with file/line numbers
- Defensive file-existence check
- Quarantine pattern: bad rows are routed aside, not silently dropped
- Validation rules stated clearly; `.copy()` used to avoid pandas warnings

## Issues to fix

| # | Issue | Why it matters | Status |
|---|-------|----------------|--------|
| 1 | Bronze filters data | Bronze should be raw, as-is. Validation/rejection belongs in silver. | [ ] |
| 2 | No lineage metadata | Add `_ingested_at`, `_source_file`, `_run_id` columns. | [ ] |
| 3 | Silent failures | Missing file logs an error and returns exit code 0. Raise or `sys.exit(1)`. | [ ] |
| 4 | Rejects have no reason | Add a `reject_reason` column to quarantined rows. | [ ] |
| 5 | One table, hardcoded | Loop over all 9 files with per-table rules in a config dict. | [ ] |
| 6 | CSV in, CSV out | Use Parquet; read IDs with `dtype=str` to avoid mangled IDs/ZIP codes. | [ ] |
| 7 | Module-level side effects | Move `makedirs` and setup into `main()`; use `getLogger(__name__)`. | [ ] |
| 8 | Emoji in log message | Can crash `FileHandler` on Windows; set `encoding="utf-8"` or drop it. | [ ] |

## Smaller improvements
- [ ] Order items use a composite key (`order_id` + `order_item_id`): check duplicates on both
- [ ] Reconciliation check: `clean + rejected == initial`; fail if reject rate is suspiciously high
- [ ] Use `pathlib`, with paths relative to the script rather than the working directory
- [ ] Stop overwriting output every run (partition by run date or `_run_id`)
- [ ] Add `.gitignore` (data, logs), `environment.yml`, README architecture diagram

## Target architecture
```
data/source (CSV) -> bronze (raw Parquet + metadata) -> silver (validated, typed, rejects flagged) -> gold
```

## Next milestones
1. Restructure bronze: land raw data untouched, plus metadata, as Parquet
2. Move validation into a separate silver step
3. Load into PostgreSQL with `bronze` and `silver` schemas
4. Simulate incremental loads (split `orders` by date)
5. Add tests and a basic orchestration step (optional: Prefect/Airflow)
