## Roadmap

- [x] Initial ingestion of `order_items` with validation and quarantine
- [ ] Bronze layer: land all 9 source files as raw Parquet with lineage metadata
- [ ] Silver layer: validation, typing and reject handling with reasons
- [ ] Load into PostgreSQL (`bronze` / `silver` schemas)
- [ ] Incremental load simulation
- [ ] Tests and orchestration

See [docs/review-notes.md](docs/review-notes.md) for detailed design notes.