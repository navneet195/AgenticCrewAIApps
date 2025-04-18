#!/bin/bash

# Ensure the script is being run from the correct directory
if [ ! -f "requirements.txt" ]; then
  echo "requirements.txt not found in the current directory!"
  exit 1
fi

# Create a virtual environment
echo "Creating a virtual environment..."
python3 -m venv crewaienv

# Activate the virtual environment
echo "Activating the virtual environment..."
source crewaienv/bin/activate

# Install required packages from requirements.txt
echo "Installing dependencies from requirements.txt..."
pip install -r requirements.txt
pip install crewai  
pip install python-pptx         

# Inform the user
echo "Environment setup complete and dependencies installed!"

# chmod +x setup.sh 
# bash setup.sh