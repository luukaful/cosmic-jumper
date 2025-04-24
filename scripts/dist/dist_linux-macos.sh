#!/bin/bash
# Step 1: Build the project into an .exe using pyinstaller
pyinstaller --onefile --noconsole --name CosmicJumper --icon=assets/icon.ico main.py

# Step 2: Create a new folder for the build output
OUTPUT_DIR="build_output"
if [ ! -d "$OUTPUT_DIR" ]; then
  mkdir "$OUTPUT_DIR"
fi

# Step 3: Move the .exe file into the new folder
mv dist/CosmicJumper "$OUTPUT_DIR/"

# Step 4: Copy the assets folder into the new folder
cp -r assets "$OUTPUT_DIR/assets"

# Step 5: Clean up unnecessary build files
rm -rf build dist CosmicJumper.spec

if [ -f "$OUTPUT_DIR/CosmicJumper" ]; then
  echo "Build process completed successfully!"
fi

# Pause to allow the user to see the output
read -p "Press Enter to exit..."