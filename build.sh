#!/bin/bash

## Update documentation
# Remove the old documentation
rm -r ./docs/
# Make the new documentation directory
mkdir ./docs/
# Generate the new documentation
pdoc --output-dir ./docs src/macroecon_tools
# pdoc --output-dir ./docs --template-dir ./templates src/macroecon_tools

## Update the version number in the pyproject.toml file
# Read the current version number
current_version=$(grep -oP '(?<=version = ")[^"]*' pyproject.toml)
# Split the version number into its components
IFS='.' read -r -a version_parts <<< "$current_version"
# Increment the patch version (the last part of the version number)
version_parts[2]=$((version_parts[2] + 1))
# Join the version parts back together
new_version="${version_parts[0]}.${version_parts[1]}.${version_parts[2]}"
# Update the pyproject.toml file with the new version number
sed -i "s/version = \"$current_version\"/version = \"$new_version\"/" pyproject.toml
# Indiate new version 
echo "Version updated from $current_version to $new_version"

## Get dependencies
# Build
pip install build  
# Twine
pip install twine  

## Build the package
# Clear the old build files
rm -r dist/
# Build the package
python3 -m build
# Check build
twine check dist/*
# Upload to testpypi (export TESTPYPI_USERNAME=<username> TESTPYPI_TOKEN=<password>)
twine upload -r testpypi dist/* -u $TESTPYPI_USERNAME -p $TESTPYPI_TOKEN

# update git
git add ./docs/
git add pyproject.toml
git commit -m "Version updated from $current_version to $new_version"