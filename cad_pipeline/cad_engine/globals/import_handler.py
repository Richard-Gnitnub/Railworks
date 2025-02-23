import cadquery as cq
import logging
import os
import tempfile
from cad_pipeline.models.exported_file import ExportedFile

# Configure Logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

def import_step_subassembly(file_name: str, generator_function=None):
    """
    Attempts to import a STEP file from the database. If it doesn't exist or is invalid, 
    triggers a generator function to create it.

    :param file_name: The exact filename of the STEP file in the database.
    :param generator_function: The function to call if the STEP file is missing or corrupted.
    :return: The imported CadQuery model or None if the process fails.
    """
    logging.info(f"🔍 Checking for existing STEP file: `{file_name}`")

    # Check if the file exists in the database
    step_file = (
        ExportedFile.objects
        .filter(file_name=file_name, file_format="step")
        .order_by("-created_at")
        .first()
    )

    if step_file:
        logging.info(f"✅ Found existing STEP file: `{file_name}`, attempting import...")
        temp_file_path = None
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".step") as temp_file:
                temp_file.write(step_file.file_data)
                temp_file_path = temp_file.name
            logging.info(f"📂 STEP file saved temporarily at `{temp_file_path}`")

            # Import the STEP file into a CadQuery Workplane
            model = cq.importers.importStep(temp_file_path)
            logging.info(f"✅ Successfully imported `{file_name}` into CadQuery.")
            return model

        except Exception as e:
            logging.warning(f"⚠️ Corrupted STEP file detected for `{file_name}`: {e}")

        finally:
            # Ensure the temporary file is removed
            if temp_file_path and os.path.exists(temp_file_path):
                os.remove(temp_file_path)
                logging.info(f"🧹 Temporary file `{temp_file_path}` deleted.")

    # If we reach here, the cached file doesn't exist or is invalid.
    logging.warning(f"⚠️ STEP file `{file_name}` not found or invalid. Attempting regeneration...")

    if generator_function:
        try:
            generated_model = generator_function()
            if generated_model:
                logging.info(f"✅ Successfully regenerated `{file_name}`.")
                return generated_model
            else:
                logging.error(f"❌ ERROR: Regeneration failed for `{file_name}`.")
                return None
        except Exception as e:
            logging.error(f"❌ ERROR: Exception during regeneration of `{file_name}`: {e}")
            return None
    else:
        logging.error("❌ ERROR: No generator function provided. Cannot proceed.")
        return None
