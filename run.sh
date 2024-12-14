#!/bin/bash

# Function to check for Python version compatibility
check_python_version() {
    required_version="3.6"
    current_version=$(python -c 'import platform; print(platform.python_version())')

    if [[ "$current_version" < "$required_version" ]]; then
        echo "Error: Python version $required_version or higher is required. You are using $current_version."
        exit 1
    fi
}

# Function to check if a package is installed
check_package() {
    python -c "import $1" &> /dev/null
    return $?
}

# Check Python version
check_python_version

# Check if numpy is installed
check_package "numpy"
if [ $? -ne 0 ]; then
    echo "Numpy is not installed."

    # Check if virtual environment exists
    if [ ! -d "auto-run-venv" ]; then
        echo "No virtual environment found. Creating one..."

        # Create a virtual environment
        python -m venv auto-run-venv

        # Activate the virtual environment based on the OS
        if [[ "$OSTYPE" == "linux-gnu"* ]]; then
            source auto-run-venv/bin/activate
        elif [[ "$OSTYPE" == "darwin"* ]]; then
            source auto-run-venv/bin/activate
        elif [[ "$OSTYPE" == "cygwin" || "$OSTYPE" == "msys" ]]; then
            source auto-run-venv/Scripts/activate
        fi
        
        # Install numpy (and other dependencies)
        echo "Installing numpy..."
        pip install numpy

        # If requirements.txt exists, install other dependencies
        if [ -f "requirements.txt" ]; then
            echo "Installing additional dependencies from requirements.txt..."
            pip install -r requirements.txt
        fi
    else
        # If virtual environment exists, activate it
        echo "Virtual environment found. Activating..."
        if [[ "$OSTYPE" == "linux-gnu"* ]]; then
            source auto-run-venv/bin/activate
        elif [[ "$OSTYPE" == "darwin"* ]]; then
            source auto-run-venv/bin/activate
        elif [[ "$OSTYPE" == "cygwin" || "$OSTYPE" == "msys" ]]; then
            source auto-run-venv/Scripts/activate
        fi
    fi
else
    echo "Numpy is already installed."
fi

# Run your python file
python main.py
