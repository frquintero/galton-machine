"""
Input validation utilities for Galton board simulation.
"""


def validate_num_balls(num_balls: int) -> None:
    """Validate number of balls parameter."""
    if not isinstance(num_balls, int):
        raise TypeError(f"num_balls must be int, got {type(num_balls).__name__}")
    if num_balls <= 0:
        raise ValueError(f"num_balls must be positive, got {num_balls}")


def validate_num_levels(num_levels: int) -> None:
    """Validate number of levels parameter."""
    if not isinstance(num_levels, int):
        raise TypeError(f"num_levels must be int, got {type(num_levels).__name__}")
    if num_levels < 0:
        raise ValueError(f"num_levels must be non-negative, got {num_levels}")


def validate_p_right(p_right: float) -> None:
    """Validate probability parameter."""
    if not isinstance(p_right, (int, float)):
        raise TypeError(f"p_right must be float, got {type(p_right).__name__}")
    if not 0.0 <= p_right <= 1.0:
        raise ValueError(f"p_right must be between 0.0 and 1.0, got {p_right}")


def validate_seed(seed) -> None:
    """Validate random seed parameter."""
    if seed is not None and not isinstance(seed, int):
        raise TypeError(f"seed must be int or None, got {type(seed).__name__}")


def validate_parameters(num_balls: int, num_levels: int, p_right: float, seed=None) -> None:
    """Validate all simulation parameters."""
    validate_num_balls(num_balls)
    validate_num_levels(num_levels)
    validate_p_right(p_right)
    validate_seed(seed)
