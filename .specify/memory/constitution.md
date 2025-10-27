<!--
Sync Impact Report:
- Version change: 1.0.0 → 1.1.0
- List of modified principles: All principles replaced (Modularity → Statistical Rigor, Error Handling → Didactic Transparency, Testing → Interactive Experiments, Documentation → Traceability of Results, Security → Portability and Zero-Friction, added Future Evolution)
- Added sections: Mission
- Removed sections: none
- Templates requiring updates: .specify/templates/plan-template.md ✅ updated
- Follow-up TODOs: none
-->

# Galton Machine Simulator Constitution

## Mission
Simulate a Galton machine in Python to teach probability, binomial distribution, and emergent normal distribution.

## Core Principles

### Statistical Rigor
The simulation must be consistent with the probabilistic model (p=0.5 left/right on each collision by default). Results must be reproducible with a seed.

### Didactic Transparency
Code and outputs must be easy to read for a high school/undergraduate student. Each important step of the process (ball drops, column counts) must be visualizable and explainable.

### Interactive Experiments
The user must be able to vary number of levels, number of balls, and bias (p≠0.5) without modifying the internal code. It must be possible to run multiple "experiments" and compare them.

### Traceability of Results
Every reported figure (final histogram, estimated mean, estimated variance) must come directly from simulated data, not hardcoded formulas.

### Portability and Zero-Friction
No heavy dependencies outside the standard library + matplotlib for graphs. Must run in console and optionally generate a figure.

### Future Evolution
The design must anticipate possible extensions: step-by-step animation, simple web interface, saving results.

## Technology and Platform Constraints
The application must be written in Python, using only the standard library plus matplotlib for plotting. It should run on Linux and other platforms without heavy dependencies, focusing on portability and ease of setup.

## Development Workflow
Development follows a structured workflow including version control with Git, code reviews for all changes, automated testing, and continuous integration. Releases should follow semantic versioning.

## Governance
This constitution guides all development decisions. Amendments require consensus among maintainers, documentation of changes, and updates to dependent artifacts. Compliance must be verified in code reviews and planning phases.

**Version**: 1.1.0 | **Ratified**: 2025-10-27 | **Last Amended**: 2025-10-27
