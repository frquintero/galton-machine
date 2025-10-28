"""
Statistical computation utilities for Galton board simulation.
"""
from typing import List


def calculate_mean(counts: List[int]) -> float:
    """
    Calculate empirical mean from counts distribution.
    
    Args:
        counts: Number of balls in each column (index = column position)
    
    Returns:
        Empirical mean of final positions
    """
    total_balls = sum(counts)
    if total_balls == 0:
        return 0.0
    
    weighted_sum = sum(column * count for column, count in enumerate(counts))
    return weighted_sum / total_balls


def calculate_variance(counts: List[int], mean: float) -> float:
    """
    Calculate population variance from counts distribution.
    
    Uses population variance formula (divide by N, not N-1) to match
    theoretical binomial variance = n * p * (1-p).
    
    Args:
        counts: Number of balls in each column
        mean: Pre-calculated mean value
    
    Returns:
        Population variance of final positions
    """
    total_balls = sum(counts)
    if total_balls == 0:
        return 0.0
    
    squared_deviations = sum(count * (column - mean) ** 2 
                             for column, count in enumerate(counts))
    return squared_deviations / total_balls


def calculate_proportions(counts: List[int]) -> List[float]:
    """
    Calculate relative frequencies from counts.
    
    Args:
        counts: Number of balls in each column
    
    Returns:
        List of proportions (frequencies) for each column
    """
    total_balls = sum(counts)
    if total_balls == 0:
        return [0.0] * len(counts)
    
    return [count / total_balls for count in counts]
