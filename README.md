# Tic Tac Toe

A clean, well-structured Tic-Tac-Toe game built with Pygame and Python 3.10

## Features

- Clean, modular code architecture
- Proper separation of concerns (game logic, UI, constants)
- Type hints throughout the codebase
- Comprehensive docstrings
- Ruff formatting and linting
- Modern Python practices

## Project Structure

```
├── src/                     # Source code directory
│   ├── __init__.py          # Package initialization
│   ├── constants.py         # All game constants and configuration
│   ├── game_logic.py        # TicTacToe class with game logic
│   ├── game_ui.py           # GameUI class for rendering and events
│   └── main.py              # Main entry point and game loop
├── tests/                   # Test suite directory
│   ├── __init__.py          # Test package initialization
│   ├── conftest.py          # Pytest fixtures and configuration
│   ├── test_constants.py    # Tests for constants module (24 tests)
│   ├── test_game_logic.py   # Tests for game logic (32 tests)
│   ├── test_game_ui.py      # Tests for UI components (25 tests)
│   └── test_main.py         # Integration tests (17 tests)
├── images/                  # Game assets directory
│   ├── welcome.png          # Welcome screen image
│   ├── x.png                # X symbol image
│   └── o.png                # O symbol image
├── .github/                 # GitHub configuration
│   └── workflows/           # GitHub Actions workflows
│       ├── code-quality.yml # Code formatting and linting checks
│       └── tests.yml        # Test execution across Python versions
├── .gitignore               # Git ignore rules
├── .python-version          # Python version specification
├── Makefile                 # Build and test commands
├── pyproject.toml           # Project configuration and dependencies
├── README.md                # Project documentation
├── ruff.toml                # Ruff configuration for formatting/linting
└── uv.lock                  # UV package manager lock file
```

## Installation

1. Clone the repository:

```bash
cd ~/Dev
mkdir ~/Dev/tic-tac-toe
cd ~/Dev/tic-tac-toe
git clone https://github.com/arvind-4/tic-tac-toe.git .
cd ~/Dev/tic-tac-toe
```

2. Create and activate virtual environment:

```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:

```bash
uv sync
```

## Running the Game

```bash
uv run src/main.py
```

## Development

### Code Formatting and Linting

This project uses Ruff for code formatting and linting:

```bash
# Format code
uv run ruff format .

# Check for linting issues
uv run ruff check .

# Fix auto-fixable issues
uv run ruff check --fix .
```

## Testing

This project includes comprehensive unit tests covering all modules and functionality.

### Running Tests

```bash
# Run all tests
uv run pytest tests/
```

## Project Organization

### Source Code Structure

- **`src/`** - All source code organized in a clean package structure
- **`tests/`** - Comprehensive test suite with 98 tests and 99% coverage
- **`images/`** - Game assets (PNG files for UI elements)

### Development Tools

- **`.gitignore`** - Comprehensive ignore rules for Python projects
- **`ruff.toml`** - Code formatting and linting configuration
- **`pyproject.toml`** - Project metadata and dependencies
- **`Makefile`** - Convenient commands for development tasks

### Virtual Environment

The project uses a virtual environment (`.venv/`) to isolate dependencies. This directory is excluded from version control.

## CI/CD Workflows

The project includes comprehensive GitHub Actions workflows for automated quality assurance.

## Requirements

- Python 3.10+
- Pygame 2.1+
- Ruff (for development)
- Pytest (for testing)
