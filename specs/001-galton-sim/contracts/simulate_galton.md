# Contract: simulate_galton

**Purpose**: Core simulation function that models ball drops through a Galton board.

**Input**:
- `num_balls`: int > 0 - Number of balls to simulate
- `num_levels`: int >= 0 - Number of decision levels
- `p_right`: float = 0.5 - Probability of moving right at each level
- `seed`: int or None = None - Random seed for reproducibility

**Output**:
- `counts`: list[int] - Ball counts per column (length = num_levels + 1)
- `mean`: float - Empirical mean of final positions
- `variance`: float - Empirical variance of final positions
- `proportions`: list[float] - Relative frequencies per column

**Behavior**:
- Each ball starts at position 0
- For each level, randomly moves right with probability p_right, left otherwise
- Final position determines column index
- Statistics calculated from actual simulation data
- If seed provided, results are deterministic

**Error Handling**:
- Raises ValueError for invalid inputs
- No side effects, pure function