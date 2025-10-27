"""
Command-line interface for Galton board simulator.
"""
import argparse
import sys
from .models import SimulationParameters
from .simulation import simulate_galton
from .rendering.ascii import render_ascii


def create_parser() -> argparse.ArgumentParser:
    """Create and configure argument parser."""
    parser = argparse.ArgumentParser(
        description="Simulate a Galton board (bean machine) to demonstrate probability",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    parser.add_argument(
        "--balls",
        type=int,
        default=1000,
        help="Number of balls to simulate"
    )
    
    parser.add_argument(
        "--levels",
        type=int,
        default=10,
        help="Number of decision levels in the board"
    )
    
    parser.add_argument(
        "--p-right",
        type=float,
        default=0.5,
        dest="p_right",
        help="Probability of going right at each level (0.0 to 1.0)"
    )
    
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Random seed for reproducibility"
    )
    
    parser.add_argument(
        "--plot",
        action="store_true",
        help="Display matplotlib plot (requires matplotlib)"
    )
    
    return parser


def format_parameters(params: SimulationParameters) -> str:
    """Format simulation parameters for display."""
    return (
        f"Parameters: balls={params.num_balls}, levels={params.num_levels}, "
        f"p_right={params.p_right}, seed={params.seed}"
    )


def format_counts(counts: list[int]) -> str:
    """Format column counts as a compact table."""
    items = [f"{i}: {count}" for i, count in enumerate(counts)]
    # Group items for readable output (max ~10 items per line)
    lines = []
    for i in range(0, len(items), 10):
        lines.append("   ".join(items[i:i+10]))
    return "\n".join(lines)


def format_statistics(mean: float, variance: float) -> str:
    """Format statistical metrics for display."""
    return f"Mean: {mean:.2f}\nVariance: {variance:.2f}"


def display_results(params: SimulationParameters, results) -> None:
    """Display simulation results to console."""
    print("\nGalton Board Simulation")
    print("=" * 23)
    print(format_parameters(params))
    print("\nColumn Counts:")
    print(format_counts(results.counts))
    print("\nStatistics:")
    print(format_statistics(results.mean, results.variance))
    print("\nASCII Histogram:")
    print(render_ascii(results.counts))


def main() -> int:
    """Main entry point for CLI."""
    parser = create_parser()
    args = parser.parse_args()
    
    try:
        # Create and validate parameters
        params = SimulationParameters(
            num_balls=args.balls,
            num_levels=args.levels,
            p_right=args.p_right,
            seed=args.seed
        )
        
        # Run simulation
        results = simulate_galton(params)
        
        # Display results
        display_results(params, results)
        
        # Handle plot if requested
        if args.plot:
            try:
                from .rendering.plot import render_plot
                render_plot(
                    results.counts,
                    params.num_levels,
                    params.p_right,
                    params.num_balls
                )
            except ImportError:
                print("\nError: matplotlib not installed.", file=sys.stderr)
                print("Install with: pip install -r requirements-plot.txt", file=sys.stderr)
                return 1
        
        return 0
        
    except (ValueError, TypeError) as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
