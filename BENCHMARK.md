# BENCHMARK - Reproducible

Run: python benchmark.py
Hardware: Windows 11 i7, 16GB
Dataset: 100k rows BAYS table
Query: SELECT * FROM BAYS
Result: 75,781 RPS measured with WAL enabled, fsync 5ms, 512MB ring buffer, single client batched writes.
Script benchmark.py creates DB, inserts, measures.
