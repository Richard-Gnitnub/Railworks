import logging
import tempfile
import cadquery as cq
from cad_pipeline.models.exported_file import ExportedFile
from cad_pipeline.cad_engine.globals.filename_handler import generate_export_filename

logging.basicConfig(level=logging.DEBUG, format="%(levelname)s: %(message)s")

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

    logging.debug(f"Export Handler: Processing component `{component.name}` with parameters: {getattr(component, 'parameters', {})}")

    # Always prioritize the user-defined filename if available
    custom_export = component.parameters.get("export_filename") if hasattr(component, "parameters") else None

    if not custom_export:
        logging.warning(f"⚠️ No custom filename found in component parameters. Deriving a name from `{component.name}`.")
        segments = component.name.split('_')
        custom_export = "_".join(segments[-3:]) if len(segments) >= 3 else segments[-1]

    logging.debug(f"Export Handler: Using `{custom_export}` as the base filename before formatting.")

    # Generate the filename using the custom name
    file_name = generate_export_filename(custom_export, "", user_defined_name=custom_export).strip('.')
    
    logging.info(f"🚀 Final export filename: `{file_name}`")

    exported_files = {}

    if not isinstance(assembly, cq.Workplane):
        logging.error(f"❌ Invalid object type: {type(assembly)}. Expected `Workplane`.")
        raise TypeError(f"Invalid object type: {type(assembly)}. Expected `Workplane`.")

    for fmt in export_formats:
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{fmt}") as tmp_file:
                temp_path = tmp_file.name

            full_file_name = f"{file_name}.{fmt}"
            logging.debug(f"📂 Exporting `{full_file_name}` to temporary file: {temp_path}")

            cq.exporters.export(assembly, temp_path)

            with open(temp_path, "rb") as file:
                file_data = file.read()
                exported_file = ExportedFile.store_exported_file(component, fmt, file_data)
                exported_files[fmt] = exported_file
                logging.info(f"✅ Successfully stored `{full_file_name}` in the database.")

        except Exception as e:
            logging.error(f"❌ Export failed for `{full_file_name}`: {e}")
            raise RuntimeError(f"Export failed for `{full_file_name}`: {e}")

    logging.info(f"✅ Export process completed for `{file_name}`.")
    return exported_files
