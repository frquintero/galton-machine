"""
Data models for Galton board simulation.
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class SimulationParameters:
    """Input configuration for a Galton board simulation."""
    
    num_balls: int
    num_levels: int
    p_right: float = 0.5
    seed: Optional[int] = None
    
    def __post_init__(self):
        """Validate parameters after initialization."""
        if self.num_balls <= 0:
            raise ValueError(f"num_balls must be > 0, got {self.num_balls}")
        if self.num_levels < 0:
            raise ValueError(f"num_levels must be >= 0, got {self.num_levels}")
        if not 0.0 <= self.p_right <= 1.0:
            raise ValueError(f"p_right must be between 0.0 and 1.0, got {self.p_right}")
        if self.seed is not None and not isinstance(self.seed, int):
            raise ValueError(f"seed must be int or None, got {type(self.seed)}")


@dataclass
class SimulationResults:
    """Output data from running a Galton board simulation."""
    
    counts: list[int]
    mean: float
    variance: float
    proportions: list[float]
    
    def __post_init__(self):
        """Validate results after initialization."""
        if len(self.counts) != len(self.proportions):
            raise ValueError("counts and proportions must have same length")
        if sum(self.counts) == 0:
            raise ValueError("counts must sum to at least 1")
