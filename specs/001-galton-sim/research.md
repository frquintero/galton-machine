# Research Findings: Galton Simulator Implementation

**Date**: 2025-10-27
**Feature**: specs/001-galton-sim/spec.md

## Python Version Selection

**Decision**: Use Python 3.8 as minimum version
**Rationale**: 
- Matplotlib 3.5+ requires Python 3.8+
- Provides good balance of modern features (walrus operator, f-strings) and compatibility
- Widely available on Linux distributions
- Allows use of typing module for better code clarity
**Alternatives considered**:
- Python 3.6: Too old, limited typing support, matplotlib compatibility issues
- Python 3.11: Latest, but may not be available on older systems; no strong need for new features

## Random Number Generation for Reproducibility

**Decision**: Use random module with seed for simulation
**Rationale**: 
- Standard library random provides sufficient quality for educational purposes
- Simple API for seeding and reproducibility
- No need for cryptographic randomness
**Alternatives considered**:
- numpy.random: Overkill for this use case, adds dependency
- secrets module: Not suitable for reproducible simulations

## ASCII Histogram Implementation

**Decision**: Custom implementation using text characters
**Rationale**: 
- No external dependencies
- Educational value in understanding histogram construction
- Simple scaling based on max count
**Alternatives considered**:
- Use external libraries: Adds dependencies, violates zero-friction principle
- Unicode block characters: Better visual but less portable across terminals

## Performance Optimization

**Decision**: Pure Python with efficient algorithms
**Rationale**: 
- O(N*L) complexity is acceptable for educational scale
- Python is fast enough for 100k operations
- Avoid premature optimization
**Alternatives considered**:
- NumPy: Could speed up but adds dependency
- Cython: Overkill for this scope