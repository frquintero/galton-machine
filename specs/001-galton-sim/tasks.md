---

description: "Task list template for feature implementation"
---

# Tasks: Galton Simulator Implementation

**Input**: Design documents from `/specs/001-galton-sim/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Tests are MANDATORY - spec.md requires 90%+ test coverage (SC-006) and statistical accuracy validation (SC-002, SC-005).

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single package**: `galton_sim/` package, `tests/` at repository root
- Paths below use the finalized structure from plan.md (no `src/` directory)
- Entry point: `galton_sim.py` at repository root

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create galton_sim/ package directory with __init__.py and rendering/ subpackage
- [ ] T002 Create requirements-plot.txt with matplotlib>=3.6 (optional dependency)
- [ ] T003 [P] Create pytest.ini for test configuration and pytest installation

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core simulation logic that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T004 Implement SimulationParameters and SimulationResults dataclasses in galton_sim/models.py
- [ ] T005 Implement simulate_galton function in galton_sim/simulation.py per contract (use local Random(seed))
- [ ] T006 Implement calculate_mean and calculate_variance in galton_sim/stats.py (compute from counts, population variance)
- [ ] T007 Implement input validation in galton_sim/validation.py

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Run Basic Simulation (Priority: P1) 🎯 MVP

**Goal**: Enable users to run a basic Galton board simulation with default parameters and view results

**Independent Test**: Run `python galton_sim.py` and verify ASCII histogram, counts, mean, and variance are displayed correctly

### Implementation for User Story 1

- [ ] T008 [US1] Implement CLI orchestration in galton_sim/cli.py with main() function
- [ ] T009 [US1] Implement argparse argument parsing in galton_sim/cli.py (default: 1000 balls, 10 levels, p=0.5)
- [ ] T010 [US1] Implement render_ascii in galton_sim/rendering/ascii.py per contract (horizontal bars, max_width=50)
- [ ] T011 [US1] Create root entry point script galton_sim.py (calls cli.main())
- [ ] T012 [US1] Add output formatting for parameters, counts table, statistics, and ASCII histogram

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Vary Simulation Parameters (Priority: P2)

**Goal**: Allow users to modify simulation parameters without code changes

**Independent Test**: Run with `--balls 2000 --levels 8 --p-right 0.6` and verify distribution shifts appropriately

### Implementation for User Story 2

- [ ] T013 [US2] Extend CLI parser to accept --balls, --levels, --p-right, --seed arguments
- [ ] T014 [US2] Integrate validation from galton_sim/validation.py in CLI flow
- [ ] T015 [US2] Update main flow to construct SimulationParameters from validated CLI args
- [ ] T016 [US2] Add error messages for invalid inputs (balls>0, levels>=0, 0<=p_right<=1)

**Checkpoint**: User Story 2 complete - parameter variation working

---

## Phase 5: User Story 3 - Generate Graphical Visualization (Priority: P3)

**Goal**: Provide optional matplotlib-based graphical output

**Independent Test**: Run with `--plot` flag and verify plot window appears with correct bar chart

### Implementation for User Story 3

- [ ] T017 [US3] Implement render_plot in galton_sim/rendering/plot.py with lazy matplotlib import
- [ ] T018 [US3] Add --plot flag to CLI parser (action='store_true')
- [ ] T019 [US3] Integrate plot display in CLI flow with try/except ImportError for matplotlib
- [ ] T020 [US3] Add helpful error message if matplotlib not installed (suggest requirements-plot.txt)

**Checkpoint**: User Story 3 complete - graphical visualization working

---

## Final Phase: Testing & Polish

**Purpose**: Quality improvements, testing, documentation, and production readiness

### Testing Tasks (Mandatory)

- [ ] T021 Create tests/unit/test_simulation.py with seed reproducibility tests
- [ ] T022 [P] Create tests/unit/test_stats.py with mean/variance accuracy tests (tolerance checks)
- [ ] T023 [P] Create tests/unit/test_rendering.py with ASCII rendering tests
- [ ] T024 [P] Create tests/unit/test_validation.py with edge case tests (balls=0, levels=0, p_right bounds)
- [ ] T025 Create tests/integration/test_cli.py with end-to-end CLI tests
- [ ] T026 Run pytest with coverage to verify 90%+ coverage requirement (SC-006)

### Polish Tasks

- [ ] T027 Add comprehensive docstrings to all public functions
- [ ] T028 Add performance test for 100k balls, 20 levels (<1s target)
- [ ] T029 Final integration testing across all user stories
- [ ] T030 Verify statistical accuracy meets SC-002 (mean/variance within 0.1 of expected)

---

## Dependencies

**User Story Completion Order**:
1. US1 (P1) - Basic simulation (MVP)
2. US2 (P2) - Parameter variation (depends on US1)
3. US3 (P3) - Visualization (depends on US1, can run parallel with US2)

**Parallel Opportunities**:
- US2 and US3 can be developed in parallel after US1 completion
- Within each story: Model/data structure tasks can run in parallel
- Rendering tasks (ASCII and plot) can run in parallel

## Implementation Strategy

**MVP Scope**: User Story 1 only - provides core educational value with basic CLI simulation

**Incremental Delivery**:
1. US1: Working simulation with text output
2. US2: Parameter flexibility 
3. US3: Visual enhancements
4. Polish: Production-ready quality

**Risk Mitigation**:
- Start with pure functions for easy testing
- Modular design allows feature toggling (plot optional)
- Statistical accuracy validation built into core logic