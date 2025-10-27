# Implementation Plan: Galton Simulator Implementation

**Branch**: `001-galton-sim` | **Date**: 2025-10-27 | **Spec**: specs/001-galton-sim/spec.md
**Input**: Feature specification from `/specs/001-galton-sim/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implement a Python CLI application that simulates a Galton board to demonstrate probability concepts. The core simulation uses probabilistic decisions for ball paths, computes statistical metrics, and provides both text and optional graphical output.

## Technical Context

**Language/Version**: Python 3.8+ (NEEDS CLARIFICATION: confirm minimum version for matplotlib compatibility)  
**Primary Dependencies**: matplotlib (for optional plotting)  
**Storage**: N/A (in-memory simulation, no persistence required)  
**Testing**: pytest (for unit and integration tests)  
**Target Platform**: Linux (primary), cross-platform compatible  
**Project Type**: single (CLI application)  
**Performance Goals**: Complete simulation of 100,000 balls with 20 levels in under 1 second  
**Constraints**: Zero heavy dependencies beyond standard library + matplotlib, console execution with optional GUI plotting  
**Scale/Scope**: Educational tool for probability learning, single-user CLI app

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- Ensure the simulation model maintains statistical rigor with correct probabilistic assumptions and reproducibility via seeds.
- Design code and outputs for didactic transparency, allowing visualization and explanation of each simulation step.
- Include interactive features for users to vary levels, balls, and bias without modifying core code, and support multiple experiment comparisons.
- Implement traceability by ensuring all reported statistics derive directly from simulated data.
- Select technologies (Python + matplotlib) that ensure portability, zero-friction setup, and console-based execution with optional plotting.
- Architect the system to anticipate future extensions like animations, web interfaces, and result saving.

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
galton_sim/                      # Main package directory
├── __init__.py                  # Package initialization
├── cli.py                       # CLI argument parsing and orchestration
├── simulation.py                # Core simulate_galton function
├── models.py                    # SimulationParameters and SimulationResults dataclasses
├── stats.py                     # Statistical computations (mean, variance)
├── validation.py                # Input parameter validation
└── rendering/                   # Output rendering modules
    ├── __init__.py
    ├── ascii.py                 # ASCII histogram rendering
    └── plot.py                  # Matplotlib plotting (lazy import)

galton_sim.py                    # Root runner script (entry point)

tests/                           # Test suite
├── unit/                        # Unit tests for individual functions
│   ├── test_simulation.py       # Core simulation logic tests
│   ├── test_stats.py            # Statistical computation tests
│   ├── test_rendering.py        # Rendering function tests
│   └── test_validation.py       # Input validation tests
└── integration/                 # Integration tests
    └── test_cli.py              # End-to-end CLI tests

requirements-plot.txt            # Optional matplotlib dependency
pytest.ini                       # Pytest configuration (if needed)
```

**Structure Decision**: Single-package layout chosen for zero-friction execution. This allows direct execution via `python galton_sim.py` without installation or PYTHONPATH manipulation. The package name matches the script name for clarity. No `src/` directory to maximize educational accessibility and simplify development workflow.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
