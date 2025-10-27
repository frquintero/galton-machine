# Contract: render_plot

**Purpose**: Generate matplotlib bar chart from simulation results.

**Input**:
- `counts`: list[int] - Ball counts per column
- `num_levels`: int - Number of levels (for title)
- `p_right`: float - Bias probability (for title)

**Output**:
- None (displays plot window)

**Behavior**:
- Creates bar chart with column indices on x-axis
- Ball counts on y-axis
- Includes title with simulation parameters
- Shows plot window (blocking or non-blocking based on implementation)

**Error Handling**:
- Raises ImportError if matplotlib not available
- Raises ValueError for invalid inputs
- May show plot window or save to file