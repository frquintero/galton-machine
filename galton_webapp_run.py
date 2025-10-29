#!/usr/bin/env python3
"""
Galton Board Web App - Entry Point

Launch the web-based interface for the Galton board simulation.
"""
import argparse
import sys
from galton_webapp.server import run


def main():
    """Main entry point for the web app."""
    parser = argparse.ArgumentParser(
        description="Launch the Galton Board Web App",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    parser.add_argument(
        "--host",
        type=str,
        default="127.0.0.1",
        help="Host address to bind to (use 0.0.0.0 for external access)"
    )
    
    parser.add_argument(
        "--port",
        type=int,
        default=5000,
        help="Port number to listen on"
    )
    
    args = parser.parse_args()
    
    try:
        run(host=args.host, port=args.port)
        return 0
    except KeyboardInterrupt:
        print("\n\nShutting down gracefully...")
        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
