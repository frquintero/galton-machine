"""
Unit tests for core simulation logic.
"""
import pytest
from galton_sim.models import SimulationParameters
from galton_sim.simulation import simulate_galton


class TestSimulationReproducibility:
    """Test that simulations with same seed produce identical results."""
    
    def test_same_seed_produces_identical_results(self):
        """Identical seeds should produce identical outputs."""
        params1 = SimulationParameters(num_balls=1000, num_levels=10, seed=42)
        params2 = SimulationParameters(num_balls=1000, num_levels=10, seed=42)
        
        results1 = simulate_galton(params1)
        results2 = simulate_galton(params2)
        
        assert results1.counts == results2.counts
        assert results1.mean == results2.mean
        assert results1.variance == results2.variance
    
    def test_different_seeds_produce_different_results(self):
        """Different seeds should (almost certainly) produce different outputs."""
        params1 = SimulationParameters(num_balls=1000, num_levels=10, seed=42)
        params2 = SimulationParameters(num_balls=1000, num_levels=10, seed=43)
        
        results1 = simulate_galton(params1)
        results2 = simulate_galton(params2)
        
        assert results1.counts != results2.counts


class TestSimulationEdgeCases:
    """Test edge cases in simulation."""
    
    def test_zero_levels_produces_single_column(self):
        """With 0 levels, all balls should end in column 0."""
        params = SimulationParameters(num_balls=100, num_levels=0, seed=42)
        results = simulate_galton(params)
        
        assert len(results.counts) == 1
        assert results.counts[0] == 100
        assert results.mean == 0.0
        assert results.variance == 0.0
    
    def test_p_right_zero_all_left(self):
        """With p_right=0.0, all balls should go left (column 0)."""
        params = SimulationParameters(num_balls=100, num_levels=10, p_right=0.0, seed=42)
        results = simulate_galton(params)
        
        assert results.counts[0] == 100
        assert all(count == 0 for count in results.counts[1:])
        assert results.mean == 0.0
        assert results.variance == 0.0
    
    def test_p_right_one_all_right(self):
        """With p_right=1.0, all balls should go right (column num_levels)."""
        params = SimulationParameters(num_balls=100, num_levels=10, p_right=1.0, seed=42)
        results = simulate_galton(params)
        
        assert results.counts[10] == 100
        assert all(count == 0 for count in results.counts[:-1])
        assert results.mean == 10.0
        assert results.variance == 0.0
    
    def test_single_ball(self):
        """Simulation should work with just one ball."""
        params = SimulationParameters(num_balls=1, num_levels=10, seed=42)
        results = simulate_galton(params)
        
        assert sum(results.counts) == 1
        assert len(results.counts) == 11


class TestSimulationStatistics:
    """Test statistical accuracy of simulation."""
    
    def test_symmetric_mean_approximation(self):
        """For p_right=0.5, mean should be approximately levels/2."""
        params = SimulationParameters(num_balls=10000, num_levels=10, p_right=0.5, seed=42)
        results = simulate_galton(params)
        
        expected_mean = 10 * 0.5
        assert abs(results.mean - expected_mean) < 0.1
    
    def test_symmetric_variance_approximation(self):
        """For p_right=0.5, variance should be approximately levels * 0.25."""
        params = SimulationParameters(num_balls=10000, num_levels=10, p_right=0.5, seed=42)
        results = simulate_galton(params)
        
        expected_variance = 10 * 0.5 * 0.5
        assert abs(results.variance - expected_variance) < 0.1
    
    def test_biased_mean_approximation(self):
        """For p_right=0.7, mean should be approximately levels * 0.7."""
        params = SimulationParameters(num_balls=10000, num_levels=10, p_right=0.7, seed=42)
        results = simulate_galton(params)
        
        expected_mean = 10 * 0.7
        assert abs(results.mean - expected_mean) < 0.1
    
    def test_biased_variance_approximation(self):
        """For p_right=0.7, variance should be approximately levels * p * (1-p)."""
        params = SimulationParameters(num_balls=10000, num_levels=10, p_right=0.7, seed=42)
        results = simulate_galton(params)
        
        expected_variance = 10 * 0.7 * 0.3
        assert abs(results.variance - expected_variance) < 0.1
    
    def test_proportions_sum_to_one(self):
        """Proportions should sum to 1.0."""
        params = SimulationParameters(num_balls=1000, num_levels=10, seed=42)
        results = simulate_galton(params)
        
        assert abs(sum(results.proportions) - 1.0) < 1e-10


class TestSimulationStructure:
    """Test structural properties of simulation results."""
    
    def test_counts_length_matches_levels(self):
        """Counts array should have num_levels + 1 elements."""
        for num_levels in [0, 5, 10, 20]:
            params = SimulationParameters(num_balls=100, num_levels=num_levels, seed=42)
            results = simulate_galton(params)
            assert len(results.counts) == num_levels + 1
    
    def test_counts_sum_to_num_balls(self):
        """Sum of counts should equal num_balls."""
        params = SimulationParameters(num_balls=1000, num_levels=10, seed=42)
        results = simulate_galton(params)
        
        assert sum(results.counts) == 1000
    
    def test_all_counts_non_negative(self):
        """All counts should be non-negative."""
        params = SimulationParameters(num_balls=1000, num_levels=10, seed=42)
        results = simulate_galton(params)
        
        assert all(count >= 0 for count in results.counts)
