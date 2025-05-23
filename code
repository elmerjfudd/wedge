#!/usr/bin/env bash
set -e

# 1. Create directory structure under the current working directory
mkdir -p "$(pwd)/summaries/csvs" \
         "$(pwd)/summaries/tables" \
         "$(pwd)/summaries/plots"

echo "Created summaries directories."

# 2. Install pip packages from requirements.txt
PYPACKS_FILE="$(pwd)/requirements.txt"
if [[ -f "$PYPACKS_FILE" ]]; then
    echo "Installing Python packages from $PYPACKS_FILE..."
    pip install -r "$PYPACKS_FILE"
else
    echo "Warning: $PYPACKS_FILE not found. Skipping pip install."
fi

# 3. Install perf tools and adjust kernel settings
echo "Updating package lists..."
sudo apt-get update

echo "Installing perf tools..."
sudo apt-get install -y linux-tools-common linux-tools-generic linux-tools-"$(uname -r)"

echo "Adjusting perf_event_paranoid..."
sudo sysctl kernel.perf_event_paranoid=-1

echo "Setup complete."
