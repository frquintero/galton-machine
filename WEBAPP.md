# Galton Board Web App

A modern, lightweight web interface for the Galton Board Simulator. Built as a separate application on top of the CLI codebase, providing an interactive browser-based experience.

## Features

- **Modern, Responsive UI**: Clean, contemporary design that works on desktop and mobile devices
- **Real-time Visualization**: Interactive Chart.js graphs with hover tooltips
- **Parameter Controls**: Intuitive sliders and inputs for simulation parameters
- **Multiple Views**: ASCII histogram, bar chart, and detailed table view
- **Zero Dependencies**: Uses only Python's standard library (`http.server`) - no external packages required
- **Zero Config**: Runs immediately - no database or complex setup required
- **Dark Mode Support**: Automatically adapts to system color preferences
- **REST API**: Simple JSON API for programmatic access

## Quick Start

### Installation

No additional dependencies required! The web app uses only Python's standard library.

### Running the Web App

```bash
# Start with default settings (localhost:5000)
python galton_webapp_run.py

# Custom host and port
python galton_webapp_run.py --host 0.0.0.0 --port 8080
```

Then open your browser to: **http://localhost:5000**

## Usage

### Web Interface

1. **Set Parameters**:
   - Number of balls (how many simulations to run)
   - Number of levels (height of the Galton board)
   - Probability of moving right (0.0 = always left, 1.0 = always right)
   - Random seed (optional, for reproducibility)

2. **Run Simulation**:
   - Click the "Simulate" button
   - View results in real-time

3. **Analyze Results**:
   - **Statistics Cards**: View mean, variance, and summary stats
   - **Interactive Chart**: Hover over bars to see exact counts
   - **ASCII Histogram**: Classic text representation
   - **Data Table**: Detailed breakdown by column

4. **Reset**: Clear results and start fresh

### API Endpoints

#### POST /api/simulate

Run a Galton board simulation.

**Request Body:**
```json
{
  "num_balls": 1000,
  "num_levels": 10,
  "p_right": 0.5,
  "seed": 42
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "counts": [0, 2, 15, 45, 120, 200, 298, 180, 95, 35, 10],
    "mean": 5.02,
    "variance": 2.48,
    "proportions": [0.0, 0.002, 0.015, 0.045, 0.12, 0.2, 0.298, 0.18, 0.095, 0.035, 0.01],
    "ascii": "...",
    "parameters": {
      "num_balls": 1000,
      "num_levels": 10,
      "p_right": 0.5,
      "seed": 42
    }
  },
  "error": null
}
```

**Error Response:**
```json
{
  "success": false,
  "data": null,
  "error": "num_balls must be > 0, got -5"
}
```

#### GET /api/health

Health check endpoint.

**Response:**
```json
{
  "status": "healthy"
}
```

## Architecture

### Technology Stack

- **Backend**: Python standard library `http.server` with `ThreadingHTTPServer`
- **Frontend**: Vanilla JavaScript + Chart.js (via CDN)
- **Styling**: Custom CSS with CSS Grid and Flexbox
- **No Build Step**: No webpack, npm, or compilation required
- **No External Dependencies**: Pure Python 3.8+ standard library

### Project Structure

```
galton_webapp/
├── __init__.py          # Package initialization
├── server.py            # HTTP server and API routes
└── templates/
    └── index.html       # Single-page web interface (Chart.js via CDN)

galton_webapp_run.py     # Web app launcher script
```

### Design Philosophy

1. **Separation of Concerns**: Web app is completely separate from CLI - different entry point, no mixing of code
2. **Lightweight**: Zero Python dependencies beyond the standard library, CDN for frontend libraries
3. **Educational**: Code is readable and well-commented for learning
4. **Modern UX**: Contemporary UI patterns and responsive design
5. **Reuses Core Logic**: Leverages the existing `galton_sim` package simulation engine

## Integration with CLI

The web app imports and uses the core simulation logic:

```python
from galton_sim.models import SimulationParameters
from galton_sim.simulation import simulate_galton
from galton_sim.rendering.ascii import render_ascii
```

This ensures:
- **Consistency**: Same simulation results as CLI
- **Maintainability**: One source of truth for core logic
- **Testing**: CLI tests validate web app behavior

## Development

### Adding New Features

1. **Backend Changes**: Edit `galton_webapp/server.py` to add new routes or modify API
2. **Frontend Changes**: Edit `galton_webapp/templates/index.html` for UI updates
3. **Testing**: Manually test in browser at http://localhost:5000

### Iterative Development

Since the server relies on the standard library, it does not include hot reloading. Restart `python galton_webapp_run.py` after making backend or template changes.

### Error Handling

The web app includes comprehensive error handling:

- **Parameter Validation**: Uses existing `SimulationParameters` validation
- **API Errors**: Returns proper HTTP status codes (400 for client errors, 500 for server errors)
- **User Feedback**: Displays error messages in the UI with clear styling

## Performance

- **Fast Simulations**: Leverages the high-performance core engine (100k balls in <1s)
- **Responsive UI**: Chart updates are optimized to prevent flickering
- **No Blocking**: Simulations run synchronously but complete quickly enough for good UX

## Browser Compatibility

- **Modern Browsers**: Chrome, Firefox, Safari, Edge (last 2 versions)
- **Mobile**: Responsive design works on tablets and phones
- **Dark Mode**: Automatically detected via `prefers-color-scheme` media query

## Comparison: Web vs CLI

| Feature | CLI | Web App |
|---------|-----|---------|
| **Installation** | Python only | Python only (no extra deps) |
| **Visualization** | ASCII + matplotlib | Interactive Chart.js |
| **Interface** | Command line | Browser-based |
| **Accessibility** | Terminal access required | Any device with browser |
| **Batch Processing** | Easy with shell scripts | Use API endpoint |
| **Educational Use** | Programming-focused | Visual learners |
| **Reproducibility** | Seed parameter | Seed parameter |

## Example Use Cases

### 1. Classroom Demonstration

Teacher runs web app on their computer, projects browser to class, and adjusts parameters in real-time to show how distributions change.

### 2. Student Exploration

Students access web app on their own devices to experiment with parameters at their own pace without needing to install Python.

### 3. Remote Learning

Share web app URL (if deployed) so remote students can run simulations without any software installation.

### 4. API Integration

Other applications can call the `/api/simulate` endpoint to generate Galton board distributions programmatically.

## Deployment

### Local Development

```bash
python galton_webapp_run.py
```

### Production Considerations

The built-in `ThreadingHTTPServer` is suitable for educational and small-scale deployment. For high-traffic production scenarios, consider using a reverse proxy like nginx in front of the Python server, or adapting the code to use a WSGI/ASGI server.

**Note**: This app is designed for educational use, not high-traffic production scenarios.

## Troubleshooting

### Port Already in Use

```bash
# Use a different port
python galton_webapp_run.py --port 8080
```

### Can't Access from Other Devices

```bash
# Bind to all interfaces
python galton_webapp_run.py --host 0.0.0.0
```

## Security Notes

- **Local Development Only**: Default binding to `127.0.0.1` prevents external access
- **No Authentication**: This is a teaching tool, not intended for multi-user production
- **Input Validation**: All parameters are validated server-side
- **No Data Storage**: Simulations run in-memory, nothing is persisted

## Future Enhancements

- **Animation Mode**: Visualize balls dropping through the board
- **Comparison Mode**: Run multiple simulations side-by-side
- **Export Results**: Download simulation data as CSV or JSON
- **Saved Configurations**: Store favorite parameter sets
- **Share Links**: Generate URLs with encoded parameters

## Contributing

When contributing to the web app:

1. Maintain separation from CLI codebase
2. Keep dependencies minimal
3. Ensure mobile responsiveness
4. Test in multiple browsers
5. Follow existing code style

## License

Same license as the main Galton Board Simulator project.
