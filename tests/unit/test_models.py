"""
Unit tests for data models.
"""
import pytest
from galton_sim.models import SimulationParameters, SimulationResults


class TestSimulationParameters:
    """Test SimulationParameters dataclass."""
    
    def test_valid_parameters(self):
        """Valid parameters should create instance."""
        params = SimulationParameters(num_balls=100, num_levels=10, p_right=0.5, seed=42)
        assert params.num_balls == 100
        assert params.num_levels == 10
        assert params.p_right == 0.5
        assert params.seed == 42
    
    def test_default_p_right(self):
        """Default p_right should be 0.5."""
        params = SimulationParameters(num_balls=100, num_levels=10)
        assert params.p_right == 0.5
    
    def test_default_seed(self):
        """Default seed should be None."""
        params = SimulationParameters(num_balls=100, num_levels=10)
        assert params.seed is None
    
    def test_zero_balls_raises_error(self):
        """Zero balls should raise ValueError."""
        with pytest.raises(ValueError, match="num_balls must be > 0"):
            SimulationParameters(num_balls=0, num_levels=10)
    
    def test_negative_balls_raises_error(self):
        """Negative balls should raise ValueError."""
        with pytest.raises(ValueError, match="num_balls must be > 0"):
            SimulationParameters(num_balls=-10, num_levels=10)
    
    def test_negative_levels_raises_error(self):
        """Negative levels should raise ValueError."""
        with pytest.raises(ValueError, match="num_levels must be >= 0"):
            SimulationParameters(num_balls=100, num_levels=-1)
    
    def test_p_right_below_zero_raises_error(self):
        """p_right below 0 should raise ValueError."""
        with pytest.raises(ValueError, match="p_right must be between"):
            SimulationParameters(num_balls=100, num_levels=10, p_right=-0.1)
    
    def test_p_right_above_one_raises_error(self):
        """p_right above 1 should raise ValueError."""
        with pytest.raises(ValueError, match="p_right must be between"):
            SimulationParameters(num_balls=100, num_levels=10, p_right=1.1)
    
    def test_invalid_seed_type_raises_error(self):
        """Non-integer seed should raise ValueError."""
        with pytest.raises(ValueError, match="seed must be int or None"):
            SimulationParameters(num_balls=100, num_levels=10, seed="not an int")


class TestSimulationResults:
    """Test SimulationResults dataclass."""
    
    def test_valid_results(self):
        """Valid results should create instance."""
        results = SimulationResults(
            counts=[10, 20, 30],
            mean=1.0,
            variance=0.5,
            proportions=[0.2, 0.3, 0.5]
        )
        assert results.counts == [10, 20, 30]
        assert results.mean == 1.0
        assert results.variance == 0.5
        assert results.proportions == [0.2, 0.3, 0.5]
    
    def test_mismatched_lengths_raises_error(self):
        """Mismatched counts and proportions lengths should raise ValueError."""
        with pytest.raises(ValueError, match="same length"):
            SimulationResults(
                counts=[10, 20, 30],
                mean=1.0,
                variance=0.5,
                proportions=[0.5, 0.5]  # Wrong length
            )
    
    def test_zero_sum_raises_error(self):
        """Zero sum of counts should raise ValueError."""
        with pytest.raises(ValueError, match="sum to at least 1"):
            SimulationResults(
                counts=[0, 0, 0],
                mean=0.0,
                variance=0.0,
                proportions=[0.0, 0.0, 0.0]
            )
