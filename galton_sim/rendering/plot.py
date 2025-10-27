"""
Matplotlib plotting for Galton board simulation results.
"""


def render_plot(counts: list[int], num_levels: int, p_right: float, num_balls: int) -> None:
    """
    Generate matplotlib bar chart from simulation results.
    
    Creates a bar chart showing the distribution of balls across columns.
    Displays in a blocking window.
    
    Args:
        counts: Number of balls in each column
        num_levels: Number of levels (for title)
        p_right: Bias probability (for title)
        num_balls: Total number of balls (for title)
    
    Raises:
        ImportError: If matplotlib is not available
        ValueError: If counts is empty
    
    Example:
        >>> counts = [1, 10, 45, 120, 90, 34, 5]
        >>> render_plot(counts, num_levels=6, p_right=0.5, num_balls=305)
        # Displays matplotlib window
    """
    # Lazy import - only load matplotlib when needed
    try:
        import matplotlib.pyplot as plt
    except ImportError as e:
        raise ImportError(
            "matplotlib is required for plotting. "
            "Install with: pip install -r requirements-plot.txt"
        ) from e
    
    if not counts:
        raise ValueError("counts cannot be empty")
    
    # Create bar chart
    columns = list(range(len(counts)))
    
    plt.figure(figsize=(10, 6))
    plt.bar(columns, counts, color='steelblue', edgecolor='black', alpha=0.7)
    
    # Labels and title
    plt.xlabel('Column (Final Position)', fontsize=12)
    plt.ylabel('Number of Balls', fontsize=12)
    plt.title(
        f'Galton Board Distribution\n'
        f'(balls={num_balls}, levels={num_levels}, p_right={p_right})',
        fontsize=14,
        fontweight='bold'
    )
    
    # Grid for easier reading
    plt.grid(axis='y', alpha=0.3, linestyle='--')
    
    # Ensure integer ticks on x-axis
    plt.xticks(columns)
    
    # Tight layout for better appearance
    plt.tight_layout()
    
    # Display plot (blocking)
    plt.show()
