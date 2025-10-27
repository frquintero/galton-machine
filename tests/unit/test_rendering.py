"""
Unit tests for rendering functions.
"""
import pytest
from galton_sim.rendering.ascii import render_ascii


class TestRenderAscii:
    """Test ASCII histogram rendering."""
    
    def test_simple_distribution(self):
        """Render simple distribution."""
        counts = [1, 5, 10, 5, 1]
        result = render_ascii(counts, max_width=10)
        
        lines = result.split('\n')
        assert len(lines) == 5
        assert all(line.startswith(f"{i:2d}:") for i, line in enumerate(lines))
    
    def test_max_count_gets_full_width(self):
        """Maximum count should get full width bar."""
        counts = [1, 5, 10, 5, 1]
        result = render_ascii(counts, max_width=10)
        
        # Line with count=10 should have 10 '#' characters
        max_line = result.split('\n')[2]
        assert max_line.count('#') == 10
    
    def test_scaling_proportional(self):
        """Bars should scale proportionally."""
        counts = [10, 20]  # 20 is twice 10
        result = render_ascii(counts, max_width=20)
        
        lines = result.split('\n')
        # First bar should be 10 chars, second should be 20
        assert lines[0].count('#') == 10
        assert lines[1].count('#') == 20
    
    def test_zero_counts(self):
        """Zero counts should produce empty bars."""
        counts = [0, 10, 0]
        result = render_ascii(counts, max_width=10)
        
        lines = result.split('\n')
        assert lines[0].count('#') == 0
        assert lines[1].count('#') == 10
        assert lines[2].count('#') == 0
    
    def test_all_zeros(self):
        """All zero counts should render without error."""
        counts = [0, 0, 0]
        result = render_ascii(counts)
        
        lines = result.split('\n')
        assert len(lines) == 3
        assert all('#' not in line for line in lines)
    
    def test_single_column(self):
        """Single column distribution."""
        counts = [100]
        result = render_ascii(counts, max_width=50)
        
        assert result.startswith(" 0:")
        assert result.count('#') == 50
    
    def test_empty_counts_raises_error(self):
        """Empty counts should raise ValueError."""
        with pytest.raises(ValueError, match="cannot be empty"):
            render_ascii([])
    
    def test_invalid_max_width_raises_error(self):
        """Invalid max_width should raise ValueError."""
        with pytest.raises(ValueError, match="max_width must be"):
            render_ascii([1, 2, 3], max_width=0)
        with pytest.raises(ValueError, match="max_width must be"):
            render_ascii([1, 2, 3], max_width=-1)
    
    def test_column_numbering(self):
        """Column numbers should be formatted correctly."""
        counts = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        result = render_ascii(counts)
        
        lines = result.split('\n')
        # Check single-digit and double-digit formatting
        assert lines[0].startswith(" 0:")
        assert lines[9].startswith(" 9:")
        assert lines[10].startswith("10:")
    
    def test_default_max_width(self):
        """Default max_width should be 50."""
        counts = [10, 20, 30]
        result = render_ascii(counts)
        
        # Max count (30) should get 50 characters
        max_line = result.split('\n')[2]
        assert max_line.count('#') == 50


class TestRenderPlot:
    """Test matplotlib plotting (import only)."""
    
    def test_plot_module_import(self):
        """Plot module should import without matplotlib."""
        import galton_sim.rendering.plot
        assert hasattr(galton_sim.rendering.plot, 'render_plot')
