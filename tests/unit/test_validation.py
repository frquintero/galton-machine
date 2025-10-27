"""
Unit tests for input validation.
"""
import pytest
from galton_sim.validation import (
    validate_num_balls,
    validate_num_levels,
    validate_p_right,
    validate_seed,
    validate_parameters
)


class TestValidateNumBalls:
    """Test validation of num_balls parameter."""
    
    def test_valid_positive_integer(self):
        """Positive integers should pass."""
        validate_num_balls(1)
        validate_num_balls(100)
        validate_num_balls(100000)
    
    def test_zero_raises_error(self):
        """Zero should raise ValueError."""
        with pytest.raises(ValueError, match="must be positive"):
            validate_num_balls(0)
    
    def test_negative_raises_error(self):
        """Negative should raise ValueError."""
        with pytest.raises(ValueError, match="must be positive"):
            validate_num_balls(-10)
    
    def test_non_integer_raises_error(self):
        """Non-integer should raise TypeError."""
        with pytest.raises(TypeError, match="must be int"):
            validate_num_balls(10.5)


class TestValidateNumLevels:
    """Test validation of num_levels parameter."""
    
    def test_valid_non_negative_integer(self):
        """Non-negative integers should pass."""
        validate_num_levels(0)
        validate_num_levels(10)
        validate_num_levels(100)
    
    def test_negative_raises_error(self):
        """Negative should raise ValueError."""
        with pytest.raises(ValueError, match="must be non-negative"):
            validate_num_levels(-1)
    
    def test_non_integer_raises_error(self):
        """Non-integer should raise TypeError."""
        with pytest.raises(TypeError, match="must be int"):
            validate_num_levels(10.5)


class TestValidatePRight:
    """Test validation of p_right parameter."""
    
    def test_valid_probability_values(self):
        """Values between 0 and 1 should pass."""
        validate_p_right(0.0)
        validate_p_right(0.5)
        validate_p_right(1.0)
        validate_p_right(0.25)
        validate_p_right(0.75)
    
    def test_below_zero_raises_error(self):
        """Values below 0 should raise ValueError."""
        with pytest.raises(ValueError, match="between 0.0 and 1.0"):
            validate_p_right(-0.1)
    
    def test_above_one_raises_error(self):
        """Values above 1 should raise ValueError."""
        with pytest.raises(ValueError, match="between 0.0 and 1.0"):
            validate_p_right(1.1)
    
    def test_non_numeric_raises_error(self):
        """Non-numeric should raise TypeError."""
        with pytest.raises(TypeError, match="must be float"):
            validate_p_right("0.5")


class TestValidateSeed:
    """Test validation of seed parameter."""
    
    def test_valid_integer_seed(self):
        """Integer seeds should pass."""
        validate_seed(0)
        validate_seed(42)
        validate_seed(-100)
    
    def test_none_seed(self):
        """None should pass."""
        validate_seed(None)
    
    def test_non_integer_raises_error(self):
        """Non-integer/non-None should raise TypeError."""
        with pytest.raises(TypeError, match="must be int or None"):
            validate_seed(42.5)
        with pytest.raises(TypeError, match="must be int or None"):
            validate_seed("42")


class TestValidateParameters:
    """Test combined parameter validation."""
    
    def test_all_valid_parameters(self):
        """All valid parameters should pass."""
        validate_parameters(1000, 10, 0.5, 42)
        validate_parameters(100, 0, 1.0, None)
    
    def test_invalid_balls_raises_error(self):
        """Invalid num_balls should raise error."""
        with pytest.raises((ValueError, TypeError)):
            validate_parameters(0, 10, 0.5, None)
    
    def test_invalid_levels_raises_error(self):
        """Invalid num_levels should raise error."""
        with pytest.raises((ValueError, TypeError)):
            validate_parameters(100, -1, 0.5, None)
    
    def test_invalid_p_right_raises_error(self):
        """Invalid p_right should raise error."""
        with pytest.raises((ValueError, TypeError)):
            validate_parameters(100, 10, 1.5, None)
    
    def test_invalid_seed_raises_error(self):
        """Invalid seed should raise error."""
        with pytest.raises(TypeError):
            validate_parameters(100, 10, 0.5, "not a seed")
