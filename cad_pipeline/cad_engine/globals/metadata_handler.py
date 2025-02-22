import logging
from datetime import datetime
from cad_pipeline.models.assembly import Assembly

logging.basicConfig(level=logging.DEBUG, format="%(levelname)s: %(message)s")

def update_computed_dimensions(assembly_name: str, dimensions: dict) -> bool:
    """
    Updates the computed dimensions metadata for the given assembly.
    Stores the dimensions under the key 'computed_dimensions' along with a timestamp.
    
    :param assembly_name: The name of the assembly to update.
    :param dimensions: A dictionary with keys like 'width', 'height', and 'depth'.
    :return: True if update succeeded, False otherwise.
    """
    try:
        assembly = Assembly.objects.get(name=assembly_name)
        # Overwrite the computed_dimensions entirely.
        assembly.parameters["computed_dimensions"] = {
            "dimensions": dimensions,
            "timestamp": datetime.now().isoformat()
        }
        assembly.save()
        logging.info(f"Updated computed dimensions for assembly '{assembly_name}': {dimensions}")
        return True
    except Assembly.DoesNotExist:
        logging.error(f"Assembly '{assembly_name}' not found. Cannot update computed dimensions.")
    except Exception as e:
        logging.error(f"Error updating computed dimensions for '{assembly_name}': {e}")
    return False

def update_last_export(assembly_name: str, export_time: str) -> bool:
    """
    Updates the last export timestamp for the given assembly.
    
    :param assembly_name: The name of the assembly.
    :param export_time: A string timestamp.
    :return: True if update succeeded, False otherwise.
    """
    try:
        assembly = Assembly.objects.get(name=assembly_name)
        assembly.parameters["last_export"] = export_time
        assembly.save()
        logging.info(f"Updated last export for assembly '{assembly_name}': {export_time}")
        return True
    except Assembly.DoesNotExist:
        logging.error(f"Assembly '{assembly_name}' not found. Cannot update last export.")
    except Exception as e:
        logging.error(f"Error updating last export for '{assembly_name}': {e}")
    return False
