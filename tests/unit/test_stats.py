"""
Unit tests for statistical calculations.
"""
import pytest
from galton_sim.stats import calculate_mean, calculate_variance, calculate_proportions


class TestCalculateMean:
    """Test mean calculation from counts."""
    
    def test_symmetric_distribution(self):
        """Mean of symmetric distribution."""
        counts = [0, 0, 1, 5, 10, 5, 1, 0, 0]
        mean = calculate_mean(counts)
        assert abs(mean - 4.0) < 0.01
    
    def test_single_value(self):
        """All balls in one column."""
        counts = [0, 0, 100, 0, 0]
        mean = calculate_mean(counts)
        assert mean == 2.0
    
    def test_empty_counts(self):
        """Empty counts returns 0."""
        counts = [0, 0, 0]
        mean = calculate_mean(counts)
        assert mean == 0.0
    
    def test_weighted_mean(self):
        """Correctly weighted mean."""
        counts = [1, 2, 3, 4]  # 0*1 + 1*2 + 2*3 + 3*4 = 20, sum=10
        mean = calculate_mean(counts)
        assert mean == 2.0


class TestCalculateVariance:
    """Test variance calculation from counts."""
    
    def test_zero_variance(self):
        """All balls in same column has zero variance."""
        counts = [0, 0, 100, 0, 0]
        mean = calculate_mean(counts)
        variance = calculate_variance(counts, mean)
        assert variance == 0.0
    
    def test_population_variance(self):
        """Variance uses population formula (divide by N)."""
        counts = [50, 50]  # mean=0.5, variance = 50*(0-0.5)^2 + 50*(1-0.5)^2 / 100 = 0.25
        mean = calculate_mean(counts)
        variance = calculate_variance(counts, mean)
        assert abs(variance - 0.25) < 0.01
    
    def test_empty_counts(self):
        """Empty counts returns 0."""
        counts = [0, 0, 0]
        variance = calculate_variance(counts, 0.0)
        assert variance == 0.0
    
    def test_known_variance(self):
        """Test with known variance value."""
        # Distribution: [10, 20, 10] at positions 0, 1, 2
        # mean = (0*10 + 1*20 + 2*10)/40 = 40/40 = 1.0
        # variance = (10*(0-1)^2 + 20*(1-1)^2 + 10*(2-1)^2)/40 = (10 + 0 + 10)/40 = 0.5
        counts = [10, 20, 10]
        mean = calculate_mean(counts)
        variance = calculate_variance(counts, mean)
        assert abs(variance - 0.5) < 0.01


class TestCalculateProportions:
    """Test proportions calculation from counts."""
    
    def test_equal_distribution(self):
        """Equal counts produce equal proportions."""
        counts = [25, 25, 25, 25]
        proportions = calculate_proportions(counts)
        assert all(abs(p - 0.25) < 0.01 for p in proportions)
    
    def test_proportions_sum_to_one(self):
        """Proportions should sum to 1.0."""
        counts = [10, 20, 30, 40]
        proportions = calculate_proportions(counts)
        assert abs(sum(proportions) - 1.0) < 1e-10
    
    def test_empty_counts(self):
        """Empty counts returns zeros."""
        counts = [0, 0, 0]
        proportions = calculate_proportions(counts)
        assert proportions == [0.0, 0.0, 0.0]
    
    def test_single_column(self):
        """All balls in one column."""
        counts = [0, 100, 0]
        proportions = calculate_proportions(counts)
        assert proportions == [0.0, 1.0, 0.0]
