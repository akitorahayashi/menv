#!/bin/bash
# pytest
alias pts="pytest"

# black
alias bl="black ."
alias bl-chk="black --check ."

# ruff
alias rf="ruff check . --fix"
alias rf-chk="ruff check ."

# python project cleanup
py-cln() {
	echo "🧹 Cleaning up project..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	rm -rf .venv
	rm -rf .pytest_cache
	rm -rf .ruff_cache
	echo "✅ Cleanup completed"
}
