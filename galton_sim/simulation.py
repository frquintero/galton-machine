"""
Core Galton board simulation logic.
"""
import random
from .models import SimulationParameters, SimulationResults
from .stats import calculate_mean, calculate_variance, calculate_proportions


def simulate_galton(params: SimulationParameters) -> SimulationResults:
    """
    Simulate ball drops through a Galton board.
    
    Each ball makes num_levels binary decisions, going right with probability
    p_right at each level. The final position (column) equals the number of
    right decisions made.
    
    Args:
        params: Simulation configuration parameters
    
    Returns:
        SimulationResults containing counts, mean, variance, and proportions
    
    Raises:
        ValueError: If parameters are invalid
    
    Example:
        >>> params = SimulationParameters(num_balls=1000, num_levels=10, seed=42)
        >>> results = simulate_galton(params)
        >>> len(results.counts)
        11
    """
    # Create local RNG for isolation (not global random state)
    rng = random.Random(params.seed)
    
    # Initialize counts array: num_levels + 1 columns (0 to num_levels)
    num_columns = params.num_levels + 1
    counts = [0] * num_columns
    
    # Simulate each ball
    for _ in range(params.num_balls):
        # Count number of "right" decisions (each with probability p_right)
        position = sum(1 for _ in range(params.num_levels) 
                      if rng.random() < params.p_right)
        counts[position] += 1
    
    # Calculate statistics from counts
    mean = calculate_mean(counts)
    variance = calculate_variance(counts, mean)
    proportions = calculate_proportions(counts)
    
    return SimulationResults(
        counts=counts,
        mean=mean,
        variance=variance,
        proportions=proportions
    )
