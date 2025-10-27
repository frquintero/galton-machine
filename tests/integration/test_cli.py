"""
Integration tests for CLI interface.
"""
import subprocess
import sys
import pytest


class TestCLIBasicExecution:
    """Test basic CLI execution."""
    
    def test_default_execution(self):
        """Run with default parameters."""
        result = subprocess.run(
            [sys.executable, "galton_sim.py"],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        assert result.returncode == 0
        assert "Galton Board Simulation" in result.stdout
        assert "Parameters:" in result.stdout
        assert "Column Counts:" in result.stdout
        assert "Statistics:" in result.stdout
        assert "ASCII Histogram:" in result.stdout
    
    def test_help_flag(self):
        """Test --help flag."""
        result = subprocess.run(
            [sys.executable, "galton_sim.py", "--help"],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        assert result.returncode == 0
        assert "usage:" in result.stdout.lower()
        assert "--balls" in result.stdout
        assert "--levels" in result.stdout
        assert "--p-right" in result.stdout


class TestCLIParameterParsing:
    """Test CLI parameter parsing."""
    
    def test_custom_balls(self):
        """Test --balls parameter."""
        result = subprocess.run(
            [sys.executable, "galton_sim.py", "--balls", "500"],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        assert result.returncode == 0
        assert "balls=500" in result.stdout
    
    def test_custom_levels(self):
        """Test --levels parameter."""
        result = subprocess.run(
            [sys.executable, "galton_sim.py", "--levels", "5"],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        assert result.returncode == 0
        assert "levels=5" in result.stdout
    
    def test_custom_p_right(self):
        """Test --p-right parameter."""
        result = subprocess.run(
            [sys.executable, "galton_sim.py", "--p-right", "0.7"],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        assert result.returncode == 0
        assert "p_right=0.7" in result.stdout
    
    def test_seed_parameter(self):
        """Test --seed parameter."""
        result = subprocess.run(
            [sys.executable, "galton_sim.py", "--seed", "42"],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        assert result.returncode == 0
        assert "seed=42" in result.stdout
    
    def test_all_parameters_combined(self):
        """Test multiple parameters together."""
        result = subprocess.run(
            [sys.executable, "galton_sim.py", 
             "--balls", "2000", "--levels", "8", "--p-right", "0.6", "--seed", "123"],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        assert result.returncode == 0
        assert "balls=2000" in result.stdout
        assert "levels=8" in result.stdout
        assert "p_right=0.6" in result.stdout
        assert "seed=123" in result.stdout


class TestCLIErrorHandling:
    """Test CLI error handling."""
    
    def test_invalid_balls(self):
        """Test invalid --balls value."""
        result = subprocess.run(
            [sys.executable, "galton_sim.py", "--balls", "0"],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        assert result.returncode == 1
        assert "Error:" in result.stderr
    
    def test_invalid_p_right(self):
        """Test invalid --p-right value."""
        result = subprocess.run(
            [sys.executable, "galton_sim.py", "--p-right", "1.5"],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        assert result.returncode == 1
        assert "Error:" in result.stderr
    
    def test_non_numeric_balls(self):
        """Test non-numeric --balls value."""
        result = subprocess.run(
            [sys.executable, "galton_sim.py", "--balls", "abc"],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        assert result.returncode != 0


class TestCLIReproducibility:
    """Test CLI reproducibility with seeds."""
    
    def test_same_seed_same_output(self):
        """Same seed should produce identical output."""
        result1 = subprocess.run(
            [sys.executable, "galton_sim.py", "--seed", "42"],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        result2 = subprocess.run(
            [sys.executable, "galton_sim.py", "--seed", "42"],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        assert result1.returncode == 0
        assert result2.returncode == 0
        assert result1.stdout == result2.stdout


class TestCLIPlotFlag:
    """Test --plot flag behavior."""
    
    def test_plot_without_matplotlib(self):
        """Test --plot flag when matplotlib not installed."""
        # This test will fail if matplotlib IS installed, but that's expected
        # It tests the error handling path
        result = subprocess.run(
            [sys.executable, "galton_sim.py", "--plot"],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        # Either succeeds (matplotlib installed) or fails with helpful message
        if result.returncode != 0:
            assert "matplotlib" in result.stderr.lower()
            assert "requirements-plot.txt" in result.stderr


class TestCLIPerformance:
    """Test CLI performance."""
    
    def test_large_simulation_completes(self):
        """Large simulation should complete in reasonable time."""
        result = subprocess.run(
            [sys.executable, "galton_sim.py", 
             "--balls", "100000", "--levels", "20"],
            capture_output=True,
            text=True,
            timeout=5  # Should complete well under 5 seconds
        )
        
        assert result.returncode == 0
        assert "balls=100000" in result.stdout
        assert "levels=20" in result.stdout
