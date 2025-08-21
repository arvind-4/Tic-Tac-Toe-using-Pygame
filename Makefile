# Makefile for Tic-Tac-Toe project

.PHONY: help install test test-verbose test-coverage lint format format-check clean run

# Default target
help:
	@echo "Available commands:"
	@echo "  install       - Install dependencies"
	@echo "  test          - Run all tests"
	@echo "  test-verbose  - Run tests with verbose output"
	@echo "  test-coverage - Run tests with coverage report"
	@echo "  lint          - Run linting checks"
	@echo "  format        - Format code with ruff"
	@echo "  format-check  - Check code formatting"
	@echo "  clean         - Clean up generated files"
	@echo "  run           - Run the game"
	@echo "  all-checks    - Run all quality checks"

# Install dependencies
install:
	pip install -e .
	pip install -r requirements.txt

# Run tests
test:
	python -m pytest tests/ -v

# Run tests with extra verbose output
test-verbose:
	python -m pytest tests/ -vv --tb=long

# Run tests with coverage
test-coverage:
	python -m pytest tests/ --cov=src --cov-report=term-missing --cov-report=html

# Run linting
lint:
	ruff check src/ tests/

# Format code
format:
	ruff format src/ tests/

# Check formatting
format-check:
	ruff format --check src/ tests/

# Clean up generated files
clean:
	rm -rf __pycache__/
	rm -rf src/__pycache__/
	rm -rf tests/__pycache__/
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	find . -name "*.pyc" -delete
	find . -name "*.pyo" -delete

# Run the game
run:
	cd src && python main.py

# Run all quality checks
all-checks: lint format-check test-coverage
	@echo "✅ All quality checks completed!"

# Quick test run (no coverage)
test-quick:
	python -m pytest tests/ -x --tb=short

# Test specific module
test-constants:
	python -m pytest tests/test_constants.py -v

test-logic:
	python -m pytest tests/test_game_logic.py -v

test-ui:
	python -m pytest tests/test_game_ui.py -v

test-main:
	python -m pytest tests/test_main.py -v

# Development setup
dev-setup: install
	@echo "Development environment setup complete!"
	@echo "Run 'make test' to verify everything works."
