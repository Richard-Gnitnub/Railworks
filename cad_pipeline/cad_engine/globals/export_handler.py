import logging
import tempfile
import cadquery as cq
from django.core.files.base import ContentFile
from cad_pipeline.models.exported_file import ExportedFile

# Configure logging
logging.basicConfig(level=logging.DEBUG, format="%(levelname)s: %(message)s")

def export_assembly(assembly, file_name, export_formats=["step", "stl"], component=None):
    """
    Exports a CadQuery Workplane and stores the result in the database.

    :param assembly: The CadQuery Workplane object to be exported.
    :param file_name: The base name for the exported files.
    :param export_formats: A list of formats to export (default: ["step", "stl"]).
    :param component: The database component associated with the exported file.
    :return: A dictionary containing exported file metadata.
    """
    logging.info(f"🚀 Starting export for {file_name} in formats: {export_formats}")
    
    exported_files = {}

    # ✅ Validate that `assembly` is a CadQuery Workplane before exporting
    if not isinstance(assembly, cq.Workplane):
        logging.error(f"❌ Invalid object type: {type(assembly)}. Expected `Workplane`.")
        raise TypeError(f"Invalid object type: {type(assembly)}. Expected `Workplane`.")

    for fmt in export_formats:
        try:
            # ✅ Create a temporary file for exporting
            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{fmt}") as tmp_file:
                temp_path = tmp_file.name

            logging.debug(f"📂 Exporting {file_name}.{fmt} to temporary file: {temp_path}")

            # ✅ Export the assembly to the specified format
            cq.exporters.export(assembly, temp_path)

            # ✅ Read the exported file
            with open(temp_path, "rb") as file:
                file_data = file.read()

                # ✅ Save to database if a component is provided
                if component:
                    exported_file = ExportedFile.store_exported_file(component, fmt, file_data)
                    exported_files[fmt] = exported_file
                    logging.info(f"✅ Successfully stored {file_name}.{fmt} in the database.")

        except Exception as e:
            logging.error(f"❌ Export failed for format {fmt}: {e}")
            raise RuntimeError(f"Export failed for format {fmt}: {e}")

    logging.info(f"✅ Export process completed for {file_name}.")
    return exported_files
