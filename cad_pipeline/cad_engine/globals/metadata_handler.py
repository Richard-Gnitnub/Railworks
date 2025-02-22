import logging
from cad_pipeline.models.assembly import Assembly

logging.basicConfig(level=logging.DEBUG, format="%(levelname)s: %(message)s")

def update_assembly_metadata(assembly_name: str, new_metadata: dict) -> bool:
    """
    Updates the metadata for a given assembly in the database by overwriting the
    'computed_dimensions' key with new_metadata.
    
    :param assembly_name: The name of the assembly to update.
    :param new_metadata: A dictionary containing metadata values (e.g., computed dimensions and timestamp).
    :return: True if the update succeeded, False otherwise.
    """
    try:
        assembly = Assembly.objects.get(name=assembly_name)
        # Overwrite the computed_dimensions key entirely.
        assembly.parameters["computed_dimensions"] = new_metadata
        assembly.save()
        logging.info(f"Updated metadata for assembly '{assembly_name}': {new_metadata}")
        return True
    except Assembly.DoesNotExist:
        logging.error(f"Assembly '{assembly_name}' not found. Cannot update metadata.")
    except Exception as e:
        logging.error(f"Error updating metadata for '{assembly_name}': {e}")
    return False
