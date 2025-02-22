import re

def generate_export_filename(assembly_name, extension, user_defined_name=None):
    """
    Generate a simplified export filename.
    
    If a user-defined name is provided (and non-empty), it is used;
    otherwise, the assembly_name is processed.
    
    Processing logic:
      - If the assembly_name contains underscores, only the last few segments are used.
      - Specifically, if there are 3 or more underscores, the last three segments are used;
        if there are fewer, the last segment is used.
      - The base name is then sanitized by replacing whitespace with underscores
        and removing any invalid characters.
    
    Parameters:
        assembly_name (str): The full name or custom name for the assembly.
        extension (str): The file extension (e.g. 'step', 'stl').
        user_defined_name (Optional[str]): A custom filename defined by the user.
    
    Returns:
        str: The generated filename.
    """
    # Use the user-defined name if provided.
    if user_defined_name and user_defined_name.strip():
        base_name = user_defined_name.strip()
    else:
        segments = assembly_name.split('_')
        if len(segments) >= 3:
            base_name = "_".join(segments[-3:])
        elif len(segments) >= 1:
            base_name = segments[-1]
        else:
            base_name = assembly_name

    # Sanitize the base name.
    base_name = re.sub(r'\s+', '_', base_name)
    base_name = re.sub(r'[^\w\-_\.]', '', base_name)
    
    return f"{base_name}.{extension}"
