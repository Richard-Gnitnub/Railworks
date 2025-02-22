#!/usr/bin/env python3
"""
Global Filename Handler
-----------------------
This module centralizes file naming logic for the project.
"""

def clean_filename(file_name: str) -> str:
    """
    Standardizes file naming conventions:
      - Removes "generate_" prefixes.
      - Converts the name to lowercase.
      - Replaces spaces with underscores.
      - Prevents duplicate parent-child naming by returning the last component if present.
    
    :param file_name: The original file name.
    :return: The cleaned file name.
    """
    file_name = file_name.replace("generate_", "").replace(" ", "_").lower()
    parts = file_name.split("_")
    return parts[-1] if len(parts) > 1 else file_name

def generate_export_filename(assembly_name: str, file_format: str) -> str:
    """
    Generates an export filename based on the assembly name and file format.
    
    :param assembly_name: The name of the assembly.
    :param file_format: The file format extension (e.g., "step").
    :return: A standardized export filename.
    """
    base_name = clean_filename(assembly_name)
    return f"{base_name}.{file_format}"
