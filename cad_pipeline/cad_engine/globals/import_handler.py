import cadquery as cq
import logging
from cad_pipeline.models.exported_file import ExportedFile

# ✅ Configure Logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

def import_step_subassembly(file_name: str, generator_function=None):
    """
    Attempts to import a STEP file from the database. If it doesn't exist, triggers a generator function to create it.
    
    :param file_name: The expected name of the STEP file in the database.
    :param generator_function: The function to call if the STEP file is missing.
    :return: The imported CadQuery model.
    """
    logging.info(f"🔍 Checking for existing STEP file: {file_name}")

    # ✅ **Check if the STEP file exists in the database**
    step_file = ExportedFile.objects.filter(file_name=file_name, file_format="step").order_by("-created_at").first()

    if step_file:
        logging.info(f"✅ Found existing STEP file: {file_name}, attempting import...")
        
        try:
            return cq.importers.importStep(step_file.file_data)  # ✅ Import stored STEP file
        except Exception as e:
            logging.warning(f"⚠️ Failed to import existing STEP file due to corruption: {e}")

    # ✅ **If the file does not exist OR is corrupted, regenerate it**
    if generator_function:
        logging.warning(f"⚠️ STEP file '{file_name}' not found or invalid. Triggering rebuild...")
        generated_model = generator_function()

        if generated_model is None:
            logging.error("❌ ERROR: Failed to generate the subassembly.")
            return None

        return generated_model
    else:
        logging.error(f"❌ ERROR: No generator function provided. Cannot proceed.")
        return None
