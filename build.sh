#!/bin/bash

# Build and Upload Script for PyPI

# Set up colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== Catapultt - PyPI Packaging ===${NC}"

# Check Python version
python_version=$(python3 --version 2>&1 | grep -oP '(?<=Python )([0-9]+\.[0-9]+)')
echo -e "${BLUE}Using Python version:${NC} $python_version"

# Clean up any existing builds
echo -e "${YELLOW}Cleaning up previous builds...${NC}"
rm -rf build/ dist/ *.egg-info/

# Install required build tools
echo -e "${BLUE}Installing build tools...${NC}"
pip install --upgrade pip build twine

# Build the package
echo -e "${BLUE}Building package...${NC}"
python -m build

# Check the package
echo -e "${BLUE}Checking package with twine...${NC}"
twine check dist/*

# Ask if user wants to upload to TestPyPI
read -p "Upload to TestPyPI? (y/N): " upload_test
if [[ $upload_test == "y" || $upload_test == "Y" ]]; then
    echo -e "${BLUE}Uploading to TestPyPI...${NC}"
    twine upload --repository-url https://test.pypi.org/legacy/ dist/*
    
    echo -e "${GREEN}Package uploaded to TestPyPI!${NC}"
    echo -e "You can test the installation with:"
    echo -e "${YELLOW}pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple catapultt${NC}"
fi

# Ask if user wants to upload to PyPI
read -p "Upload to PyPI? (y/N): " upload_pypi
if [[ $upload_pypi == "y" || $upload_pypi == "Y" ]]; then
    echo -e "${BLUE}Uploading to PyPI...${NC}"
    twine upload dist/*
    
    echo -e "${GREEN}Package uploaded to PyPI!${NC}"
    echo -e "Your package is now available at: https://pypi.org/project/catapultt/"
    echo -e "Users can install it with: ${YELLOW}pip install catapultt${NC}"
else
    echo -e "${YELLOW}Not uploading to PyPI. You can do this later with:${NC}"
    echo -e "${YELLOW}twine upload dist/*${NC}"
fi

echo -e "${GREEN}Build process complete!${NC}"