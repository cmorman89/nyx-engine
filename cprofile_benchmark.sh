#!/bin/bash

# Find the current script's directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Define the output directory and ensure it exists
OUTPUT_DIR="$SCRIPT_DIR/.logs/profiles/cprofile"
mkdir -p "$OUTPUT_DIR"

# Generate the dynamic filename with the current timestamp
TIMESTAMP="$(date +"%Y-%m-%d_%H-%M-%S")"
OUTPUT_FILE="$OUTPUT_DIR/cprofile-$TIMESTAMP.prof"

# Open main.py in the same directory as the script and profile it
"$SCRIPT_DIR/.venv/bin/python" -m cProfile -o "$OUTPUT_FILE" "$SCRIPT_DIR/main.py"

# Ask if the user wants to rename the file
echo "Profile output saved to: $OUTPUT_FILE"
read -p "Do you wish to rename the output file? (y/n): " RESPONSE
if [[ "$RESPONSE" == "y" || "$RESPONSE" == "Y" ]]; then
    read -p "Enter new filename (without path): " NEW_FILENAME
    mv "$OUTPUT_FILE" "$OUTPUT_DIR/$NEW_FILENAME"
    echo "File renamed to: $OUTPUT_DIR/$NEW_FILENAME"
fi