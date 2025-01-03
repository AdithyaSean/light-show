#!/bin/bash

# Exit on error
set -e

# Create and activate virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv

    # Check Python version
    python3 --version

    # Activate virtual environment
    echo "Activating virtual environment..."
    source .venv/bin/activate

    # Upgrade pip and setuptools first
    echo "Upgrading pip and setuptools..."
    pip install --upgrade pip setuptools wheel

    # Install requirements
    echo "Installing requirements..."
    pip install -r requirements.txt

    # Run the LED show
    echo "Starting LED show..."
    python led_show.py

else
    # Activate virtual environment
    echo "Activating virtual environment..."
    source .venv/bin/activate

    # Run the LED show
    echo "Starting LED show..."
    python led_show.py
fi
