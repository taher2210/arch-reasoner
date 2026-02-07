#!/bin/bash
# Arch-Reasoner wrapper script
# Activates virtual environment and runs the main Python script

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Activate virtual environment
source "$SCRIPT_DIR/venv/bin/activate"

# Run the Python script with all arguments
python "$SCRIPT_DIR/arch_agent.py" "$@"
