# Quick Start: Galton Simulator

**Date**: 2025-10-27
**Feature**: specs/001-galton-sim/spec.md

## Prerequisites

- Python 3.8+
- matplotlib (optional, for plotting)

## Installation

```bash
# Clone repository
git clone <repository-url>
cd galton-sim

# Install matplotlib (optional)
pip install matplotlib
```

## Basic Usage

Run a default simulation:

```bash
python galton_sim.py
```

This simulates 1000 balls through 10 levels with p=0.5.

## Command Line Options

```bash
python galton_sim.py [OPTIONS]

Options:
  --balls INT      Number of balls (default: 1000)
  --levels INT     Number of levels (default: 10)
  --p-right FLOAT  Probability of going right (default: 0.5)
  --seed INT       Random seed for reproducibility
  --plot           Generate matplotlib plot
  --help           Show help message
```

## Examples

Run with custom parameters:

```bash
python galton_sim.py --balls 5000 --levels 12 --p-right 0.6
```

Reproducible simulation:

```bash
python galton_sim.py --balls 1000 --levels 10 --seed 42
```

With visualization:

```bash
python galton_sim.py --balls 5000 --levels 10 --plot
```

## Expected Output

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
 0: #
 1: ###
 2: ##########
 3: ##################
 4: ########################################
 5: #######################################################
 6: #################################################################################
 7: #####################################################################
 8: ##################################
 9: #############
10: ######

```

## Troubleshooting

- If matplotlib is not installed, --plot will show an error message
- Large simulations (>100k balls) may take a few seconds
- Use --seed for consistent results when debugging