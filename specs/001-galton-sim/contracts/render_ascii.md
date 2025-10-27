# Contract: render_ascii

**Purpose**: Generate ASCII text histogram from simulation results.

**Input**:
- `counts`: list[int] - Ball counts per column
- `max_width`: int = 50 - Maximum width of histogram bars

**Output**:
- `histogram`: str - Multi-line ASCII histogram string

**Behavior**:
- Creates horizontal bar chart with column indices
- Scales bars proportionally to max count
- Uses simple text characters (# or *)
- Includes column labels and counts

**Error Handling**:
- Raises ValueError for invalid counts
- No side effects