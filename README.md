# Olympiad Data Processing (2026/27 Season)

This workspace contains the data processing pipeline and schedule tables for RSOSH school olympiads for the 2026/27 academic year across three tracks:
1. **Informatics** (Computer Science) — 18 olympiads
2. **Mathematics** — 21 olympiads
3. **Artificial Intelligence** — 3 olympiads

## Files in Repository
- `olympiads_2026_27.html`: Main HTML output containing the verified tables.
- `SPEC.md`: Full specification (tasks 1 & 6) — formatting rules, venue logic, and tracked olympiads.
- `check_sites.py`: Python script to fetch and check official olympiad websites for schedule updates.
- `validate_table.py`: Validation script ensuring table structure, row counts, venue formats (`отбор: ...; финал: ...`), and date bolding rules (`season-2026` / `<b>`).

## Usage

### 1. Validate Table Structure and Rules
```bash
python3 validate_table.py
```

### 2. Check Official Websites for Schedule Updates
```bash
python3 check_sites.py
```
