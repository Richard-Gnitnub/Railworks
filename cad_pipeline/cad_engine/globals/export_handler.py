import logging
import tempfile
import cadquery as cq
from cad_pipeline.models.exported_file import ExportedFile

# ✅ Configure Logging
logging.basicConfig(level=logging.DEBUG, format="%(levelname)s: %(message)s")

def clean_filename(file_name):
    """
    Standardize file naming convention globally.
    - Removes "generate_" prefixes.
    - Ensures lowercase and underscores.
    - Prevents duplicate parent-child naming.
    - Keeps only the most relevant name component.
    """
    file_name = file_name.replace("generate_", "").replace(" ", "_").lower()
    parts = file_name.split("_")

    # ✅ Avoid redundant parent-child names
    return parts[-1] if len(parts) > 1 else file_name

def export_assembly(assembly, export_formats=["step", "stl"], component=None):
    """
    Exports a CadQuery Workplane and stores the result in the database.

    :param assembly: The CadQuery Workplane object to be exported.
    :param export_formats: A list of formats to export (default: ["step", "stl"]).
    :param component: The database component associated with the exported file.
    :return: A dictionary containing exported file metadata.
    """
    if component is None:
        logging.error("❌ ERROR: `export_assembly()` requires a component to determine filename.")
        raise ValueError("`export_assembly()` requires a component.")

    # ✅ Extract and clean filename correctly
    original_name = component.name
    file_name = clean_filename(original_name)  
    logging.info(f"🚀 Cleaning filename: `{original_name}` → `{file_name}`")

    exported_files = {}

    if not isinstance(assembly, cq.Workplane):
        logging.error(f"❌ Invalid object type: {type(assembly)}. Expected `Workplane`.")
        raise TypeError(f"Invalid object type: {type(assembly)}. Expected `Workplane`.")

    for fmt in export_formats:
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{fmt}") as tmp_file:
                temp_path = tmp_file.name

            logging.debug(f"📂 Exporting `{file_name}.{fmt}` to temporary file: {temp_path}")

            cq.exporters.export(assembly, temp_path)

            with open(temp_path, "rb") as file:
                file_data = file.read()
                exported_file = ExportedFile.store_exported_file(component, fmt, file_data)
                exported_files[fmt] = exported_file
                logging.info(f"✅ Successfully stored `{file_name}.{fmt}` in the database.")

        except Exception as e:
            logging.error(f"❌ Export failed for `{file_name}.{fmt}`: {e}")
            raise RuntimeError(f"Export failed for `{file_name}.{fmt}`: {e}")

    logging.info(f"✅ Export process completed for `{file_name}`.")
    return exported_files
