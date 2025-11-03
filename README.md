# Eval_Search-and-Optimization-Algorithms
This project implements key search and optimization algorithms in Python for a university Intelligent Systems assignment. It features BFS, IDS, A*, Simulated Annealing, Dynamic Programming, and Linear Programming on a 2D grid with obstacles, plus a runner that tests, compares, and reports results.

## Viewing Results

The project generates an HTML report (`index.html`) that visualizes all results. To view it properly:

### Option 1: Local HTTP Server (Recommended)
```bash
# Start a local server in the project directory
python3 -m http.server 8000

# Then open in your browser:
# http://localhost:8000/index.html
```

### Option 2: Direct File Access
If you open `index.html` directly (file:// protocol), you may encounter CORS errors preventing JSON loading. The HTML now includes helpful error messages to guide you.

**Why?** Browsers block JavaScript from fetching local files when opened via `file://` for security reasons.
