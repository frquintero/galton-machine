# Galton Board Simulator

A Python CLI application that simulates a Galton board (bean machine) to demonstrate probability concepts and the emergence of normal distributions from binomial processes.

## Overview

The Galton board is a classical probability demonstration device where balls drop through levels of pegs, randomly bouncing left or right at each level. This simulator provides a computational model of the Galton board with statistical analysis and visualization capabilities.

## Features

- **Probabilistic Simulation**: Simulates N balls dropping through L levels with configurable bias
- **Statistical Analysis**: Computes empirical mean, variance, and distribution proportions
- **ASCII Visualization**: Console-based histogram for universal accessibility
- **Graphical Output**: Optional matplotlib-based bar charts
- **Reproducibility**: Seed-based random number generation for consistent results
- **Performance**: Handles 100,000 balls with 20 levels in under 1 second

## Prerequisites

- Python 3.8+
- matplotlib (optional, for graphical visualization)

## Installation

```bash
# Clone repository
git clone <repository-url>
cd galton-sim

# Install matplotlib (optional)
pip install matplotlib
```

## Quick Start

Run a basic simulation with default parameters (1000 balls, 10 levels, p=0.5):

```bash
python galton_sim.py
```

## Usage

```bash
python galton_sim.py [OPTIONS]
```

### Command Line Options

- `--balls INT` - Number of balls to simulate (default: 1000)
- `--levels INT` - Number of decision levels (default: 10)
- `--p-right FLOAT` - Probability of going right at each level (default: 0.5)
- `--seed INT` - Random seed for reproducibility
- `--plot` - Generate matplotlib visualization
- `--help` - Show help message

### Examples

**Custom Parameters:**
```bash
python galton_sim.py --balls 5000 --levels 12 --p-right 0.6
```

**Reproducible Simulation:**
```bash
python galton_sim.py --seed 42
```

**With Visualization:**
```bash
python galton_sim.py --balls 5000 --levels 10 --plot
```

**Biased Distribution:**
```bash
python galton_sim.py --balls 10000 --levels 15 --p-right 0.7 --plot
```

## Output

The simulator provides:

1. **Simulation Parameters**: Displays input configuration
2. **Column Counts**: Number of balls in each output column
3. **Statistical Metrics**:
   - Empirical mean (expected: `levels × p_right`)
   - Empirical variance (expected: `levels × p_right × (1 - p_right)`)
4. **ASCII Histogram**: Text-based visualization of the distribution
5. **Graphical Plot** (optional): Matplotlib bar chart

### Sample Output

```
Galton Board Simulation
=======================
Parameters: balls=5000, levels=10, p_right=0.5, seed=None

Column Counts:
0: 1    1: 8    2: 45   3: 171  4: 430  5: 735  6: 876  7: 688  8: 345  9: 123  10: 28

Statistics:
Mean: 5.00
Variance: 2.50

ASCII Histogram:
 0: # (1 ball)
 1: ### (8 balls)
 2: ########## (45 balls)
 3: ################## (171 balls)
 4: ######################################## (430 balls)
 5: ####################################################### (735 balls)
 6: ################################################################################# (876 balls)
 7: ##################################################################### (688 balls)
 8: ################################## (345 balls)
 9: ############# (123 balls)
10: ###### (28 balls)
```

## Architecture

### Core Components

- **SimulationParameters**: Input data class (num_balls, num_levels, p_right, seed)
- **SimulationResults**: Output data class (counts, mean, variance, proportions)
- **simulate_galton()**: Pure simulation function with no side effects
- **render_ascii()**: Text-based histogram generator
- **render_plot()**: Matplotlib visualization generator
- **CLI Interface**: Argument parsing and output formatting

### Design Principles

- **Modularity**: Core simulation logic separated from rendering and CLI
- **Pure Functions**: Simulation engine has no dependencies on UI or plotting libraries
- **Determinism**: Reproducible results via seed control
- **Performance**: O(N×L) complexity for N balls and L levels
- **Educational Focus**: Clear code structure for learning purposes

## Educational Use Cases

### User Story 1: Basic Simulation
Students can run a basic simulation to observe how a binomial process creates a bell-shaped (normal) distribution.

### User Story 2: Parameter Exploration
Teachers can vary parameters to demonstrate:
- Effect of sample size on distribution smoothness
- Impact of bias (p_right ≠ 0.5) on distribution shape
- Relationship between levels and variance

### User Story 3: Visual Learning
Visual learners can use the `--plot` option to see graphical representations of probability distributions.

## Project Structure

```
galton-sim/
├── galton_sim/                  # Main package directory
│   ├── __init__.py              # Package initialization
│   ├── cli.py                   # CLI argument parsing and orchestration
│   ├── simulation.py            # Core simulate_galton function
│   ├── models.py                # SimulationParameters and SimulationResults dataclasses
│   ├── stats.py                 # Statistical computations (mean, variance)
│   ├── validation.py            # Input parameter validation
│   └── rendering/               # Output rendering modules
│       ├── __init__.py
│       ├── ascii.py             # ASCII histogram rendering
│       └── plot.py              # Matplotlib plotting (lazy import)
├── tests/                       # Test suite
│   ├── unit/                    # Unit tests for individual functions
│   │   ├── test_simulation.py   # Core simulation logic tests
│   │   ├── test_stats.py        # Statistical computation tests
│   │   ├── test_rendering.py    # Rendering function tests
│   │   └── test_validation.py   # Input validation tests
│   └── integration/             # Integration tests
│       └── test_cli.py          # End-to-end CLI tests
├── specs/
│   └── 001-galton-sim/          # Feature specification documents
├── galton_sim.py                # Root entry point script
├── requirements-plot.txt        # Optional matplotlib dependency
├── AGENTS.md                    # Developer guide for AI agents
└── README.md                    # This file
```

## Development

### Implementation Phases

1. **Phase 1**: Setup - Project structure and dependencies
2. **Phase 2**: Foundation - Core simulation logic and data models
3. **Phase 3**: User Story 1 - Basic CLI simulation with ASCII output
4. **Phase 4**: User Story 2 - Parameter variation support
5. **Phase 5**: User Story 3 - Graphical visualization
6. **Final Phase**: Polish - Error handling, documentation, optimization

### Testing

Tests are mandatory to ensure statistical accuracy and reproducibility. Use pytest:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=galton_sim --cov-report=term-missing

# Target: 90%+ coverage
```

## Performance Targets

- 100,000 balls with 20 levels: < 1 second
- Statistical accuracy: Mean and variance within 0.1 of theoretical values
- Code coverage: 90%+ for simulation logic

## Edge Cases

- `num_balls = 0`: Rejected with error
- `num_levels = 0`: Produces 1 column with all balls
- `p_right = 0.0`: All balls go left (deterministic)
- `p_right = 1.0`: All balls go right (deterministic)

## Troubleshooting

- **matplotlib not installed**: `--plot` will show an error; install with `pip install matplotlib`
- **Large simulations slow**: For >100k balls, expect a few seconds processing time
- **Inconsistent results**: Use `--seed` parameter for reproducibility

## Future Enhancements

- Animation of ball drops
- Web interface for interactive exploration
- Result saving to CSV/JSON
- Multiple experiment comparison
- Visual representation of individual ball paths

## License

[To be determined]

## Contributing

This is an educational project. Contributions should maintain code clarity and educational value.

## Specification

For detailed specifications, see [specs/001-galton-sim/spec.md](specs/001-galton-sim/spec.md)

## Documentation

- [Implementation Plan](specs/001-galton-sim/plan.md)
- [Task Breakdown](specs/001-galton-sim/tasks.md)
- [Data Model](specs/001-galton-sim/data-model.md)
- [Quick Start Guide](specs/001-galton-sim/quickstart.md)
- [Research Findings](specs/001-galton-sim/research.md)
- [Function Contracts](specs/001-galton-sim/contracts/)
