# Data Model: Galton Simulator Implementation

**Date**: 2025-10-27
**Feature**: specs/001-galton-sim/spec.md

## Entities

### SimulationParameters
Represents the input configuration for a Galton board simulation.

**Fields**:
- `num_balls`: int > 0 - Number of balls to simulate
- `num_levels`: int >= 0 - Number of levels (decision points) in the board
- `p_right`: float 0.0 to 1.0 - Probability of going right at each level (default 0.5)
- `seed`: int or None - Random seed for reproducible results

**Validation Rules**:
- num_balls must be positive integer
- num_levels must be non-negative integer
- p_right must be between 0.0 and 1.0 inclusive
- seed must be integer or None

**Relationships**: Input to SimulationResults

### SimulationResults
Represents the output data from running a simulation.

**Fields**:
- `counts`: list[int] - Number of balls in each column (length = num_levels + 1)
- `mean`: float - Empirical mean of final positions
- `variance`: float - Empirical variance of final positions
- `proportions`: list[float] - Relative frequency for each column (length = num_levels + 1)

**Validation Rules**:
- counts length must equal num_levels + 1
- all counts must be non-negative integers summing to num_balls
- mean and variance must be calculable floats
- proportions must sum to 1.0 (within floating point precision)

**Relationships**: Generated from SimulationParameters

## Data Flow

1. User provides SimulationParameters
2. Simulation engine processes parameters to generate SimulationResults
3. Results are displayed via CLI and optionally plotted
4. No persistence required - results are ephemeral