#!/bin/bash
# Run the sales forecasting pipeline
# Usage: ./run_pipeline.sh

set -e

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Activate virtual environment if it exists
if [ -f ~/data-tools/bin/activate ]; then
    source ~/data-tools/bin/activate
fi

# Run the pipeline
echo "Starting sales forecasting pipeline..."
echo "Time: $(date)"
echo "========================================"

python -m src.pipeline

echo "========================================"
echo "Pipeline completed at: $(date)"
