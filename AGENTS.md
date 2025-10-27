# AGENTS.md - Developer Guide for Galton Board Simulator

This file provides essential information for AI agents and developers working on this project.

## Project Overview

**Name**: Galton Board Simulator  
**Type**: Python CLI application  
**Purpose**: Educational tool demonstrating probability concepts through Galton board simulation  
**Python Version**: 3.8+  

## Commands

### Running the Application

```bash
# Basic execution with defaults (1000 balls, 10 levels, p=0.5)
python galton_sim.py

# With custom parameters
python galton_sim.py --balls 5000 --levels 12 --p-right 0.6

# With reproducible seed
python galton_sim.py --seed 42

# With matplotlib visualization (requires optional dependency)
python galton_sim.py --plot
```

### Testing

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=galton_sim --cov-report=term-missing

# Run specific test file
pytest tests/unit/test_simulation.py

# Run tests in parallel (if pytest-xdist installed)
pytest -n auto

# Target: 90%+ coverage (SC-006 from spec.md)
```

### Dependencies

```bash
# Install optional plotting dependency
pip install -r requirements-plot.txt

# Install development dependencies (pytest, coverage)
pip install pytest pytest-cov
```

## Code Style & Conventions

### Naming Conventions

- **Functions**: `snake_case` - e.g., `simulate_galton`, `render_ascii`
- **Classes**: `PascalCase` - e.g., `SimulationParameters`, `SimulationResults`
- **Constants**: `UPPER_SNAKE_CASE` - e.g., `DEFAULT_NUM_BALLS`
- **Variables**: `snake_case` - e.g., `num_balls`, `p_right`

### Module Organization

```
galton_sim/
├── models.py          # Data classes (use @dataclass)
├── simulation.py      # Core simulation logic (pure functions)
├── stats.py           # Statistical calculations
├── validation.py      # Input validation
├── cli.py             # CLI orchestration and argparse
└── rendering/
    ├── ascii.py       # Text-based output
    └── plot.py        # Matplotlib output (lazy import)
```

### Key Design Principles

1. **Pure Functions**: Core simulation has no side effects
2. **Local RNG**: Use `random.Random(seed)` for isolated randomness, not global `random`
3. **Lazy Imports**: Import matplotlib only when `--plot` is used
4. **Population Variance**: Use `variance = levels * p * (1-p)`, not sample variance
5. **Zero Dependencies**: Core functionality works without matplotlib
6. **Educational Clarity**: Code should be readable by students learning probability

## Architecture Notes

### Data Flow

```
CLI Args → Validation → SimulationParameters → simulate_galton() → SimulationResults → Rendering
```

### Key Contracts

- **simulate_galton**: Pure function, O(N×L) complexity, deterministic with seed
- **render_ascii**: Takes counts array, returns string (max_width=50)
- **render_plot**: Takes counts + params, displays matplotlib window or warns if unavailable

### Statistical Correctness

- **Mean**: Should be approximately `num_levels × p_right`
- **Variance**: Should be approximately `num_levels × p_right × (1 - p_right)`
- **Tolerance**: Within 0.1 for large N (per SC-002)

## Performance Requirements

- **Target**: 100,000 balls with 20 levels in < 1 second (SC-001)
- **Complexity**: O(N×L) where N=balls, L=levels
- **Optimization**: Avoid per-ball printing; scale bars to max count, not total balls

## Testing Requirements

### Mandatory Test Coverage

- **Unit Tests**:
  - Seed reproducibility (identical outputs with same seed)
  - Edge cases: `levels=0`, `p_right=0.0`, `p_right=1.0`, invalid inputs
  - Statistical accuracy (mean/variance within tolerance)
  - ASCII rendering correctness
  
- **Integration Tests**:
  - End-to-end CLI execution
  - Parameter parsing and validation
  - Matplotlib availability handling

- **Coverage Target**: 90%+ (SC-006)

## Common Issues & Solutions

### Issue: "ModuleNotFoundError: No module named 'matplotlib'"

**Solution**: Matplotlib is optional. Either:
- Install with `pip install -r requirements-plot.txt`
- Run without `--plot` flag for text-only output

### Issue: Results not reproducible

**Solution**: Use `--seed` parameter for deterministic results:
```bash
python galton_sim.py --seed 42
```

### Issue: Large simulations slow

**Expected**: 100k balls should complete in ~1 second. Larger values may take longer.

## Development Workflow

1. **Before coding**: Review specs in `specs/001-galton-sim/`
2. **Implementation order**: Follow phases in `specs/001-galton-sim/tasks.md`
3. **Testing**: Write tests alongside implementation (TDD encouraged)
4. **Validation**: Run `pytest --cov` before considering task complete

## Future Extensions (Documented in README.md)

- Animation of ball drops
- Web interface
- CSV/JSON export
- Multiple experiment comparison
- Individual ball path visualization

## Specification References

- Main spec: `specs/001-galton-sim/spec.md`
- Implementation plan: `specs/001-galton-sim/plan.md`
- Task breakdown: `specs/001-galton-sim/tasks.md`
- Data model: `specs/001-galton-sim/data-model.md`
- Function contracts: `specs/001-galton-sim/contracts/`
