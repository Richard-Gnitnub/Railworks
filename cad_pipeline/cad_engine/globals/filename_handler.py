import re
import logging

logging.basicConfig(level=logging.DEBUG, format="%(levelname)s: %(message)s")

def generate_export_filename(assembly_name, extension, user_defined_name=None):
    """
    Generate a simplified export filename.
    
    If a user-defined name is provided, it takes priority.
    Otherwise, the assembly_name is processed to extract a concise filename.

    Processing logic:
      - If `user_defined_name` exists, use it directly.
      - If `assembly_name` contains underscores, extract only the last few segments.
      - If no underscores exist, use the full `assembly_name`.
      - Finally, sanitize the filename to remove any invalid characters.

    Parameters:
        assembly_name (str): The full name of the assembly.
        extension (str): The file extension (e.g. 'step', 'stl').
        user_defined_name (Optional[str]): A custom filename defined by the user.

    Returns:
        str: The generated filename.
    """
    logging.debug(f"Filename Handler: Received assembly_name='{assembly_name}', extension='{extension}', user_defined_name='{user_defined_name}'")

    # Prioritize user-defined filename
    if user_defined_name and user_defined_name.strip():
        base_name = user_defined_name.strip()
        logging.debug(f"Filename Handler: Using user-defined name `{base_name}`")
    else:
        segments = assembly_name.split('_')
        base_name = "_".join(segments[-3:]) if len(segments) >= 3 else segments[-1]
        logging.debug(f"Filename Handler: Derived name `{base_name}` from assembly_name `{assembly_name}`")

    # Sanitize the base name
    base_name = re.sub(r'\s+', '_', base_name)
    base_name = re.sub(r'[^\w\-_\.]', '', base_name)

    final_filename = f"{base_name}.{extension}".strip('.')
    logging.debug(f"Filename Handler: Returning filename `{final_filename}`")
    
    return final_filename
