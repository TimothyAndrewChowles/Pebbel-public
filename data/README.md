# Data

The source T12 workbooks are private and are not stored in this repository.

For this experiment, the working dataset is derived from the private corpus after deterministic parsing and cleaning.

## Current corpus summary

- 350 source files profiled
- 348 genuine workbooks
- 342 candidate T12 statements
- 53 byte-identical duplicates identified
- 73,726 account lines extracted
- 67,108 rows had a usable total for validation
- 65,593 of those rows passed the row-sum check (97.7%)

## Cleaning rules

1. Reject non-T12 and unsupported files.
2. Use sanitized workbook IDs.
3. Normalize month and period columns.
4. Extract account rows deterministically.
5. Preserve values as decimals.
6. Flag unresolved cases instead of guessing.
7. Prevent duplicate files from crossing train/validation/test boundaries.
8. Freeze the final held-out test set before tuning.

Only sanitized or synthetic examples should be committed here.
