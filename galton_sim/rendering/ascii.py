"""
ASCII histogram rendering for Galton board simulation results.
"""


def render_ascii(counts: list[int], max_width: int = 50) -> str:
    """
    Generate ASCII text histogram from simulation results.
    
    Creates horizontal bar chart with column indices and proportional bar widths.
    Bars are scaled to fit within max_width characters.
    
    Args:
        counts: Number of balls in each column
        max_width: Maximum width of histogram bars in characters
    
    Returns:
        Multi-line ASCII histogram string
    
    Raises:
        ValueError: If counts is empty or max_width < 1
    
    Example:
        >>> counts = [1, 10, 45, 120, 90, 34, 5]
        >>> print(render_ascii(counts, max_width=30))
         0: #
         1: ##
         2: ##########
         3: ##############################
         4: ######################
         5: ########
         6: #
    """
    if not counts:
        raise ValueError("counts cannot be empty")
    if max_width < 1:
        raise ValueError(f"max_width must be >= 1, got {max_width}")
    
    max_count = max(counts)
    if max_count == 0:
        # All counts are zero
        return "\n".join(f"{i:2d}:" for i in range(len(counts)))
    
    lines = []
    for column, count in enumerate(counts):
        # Scale bar width proportionally to max count
        bar_width = int((count / max_count) * max_width)
        bar = "#" * bar_width
        lines.append(f"{column:2d}: {bar}")
    
    return "\n".join(lines)
