# Swagger Documentation Generator

This project is a Python script that generates API documentation from a Swagger JSON file.

## Features
- Parses a Swagger JSON file
- Generates structured API documentation
- Supports various output formats

## Requirements
- Python 3.12.6
- Required dependencies (install via `requirements.txt`):
  ```bash
  pip install -r requirements.txt
  ```

## Usage
1. Create a new folder called "ToBeProcessed" in the project directory.
2. Place your "swagger.json" file in the new folder.
3. Run the main.py file:
4. The generated documentation will be saved in the "GeneratedDocs", the "swagger.json" file will be moved to Process/{datetime} .
