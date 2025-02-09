import tempfile
import cadquery as cq
from django.core.files.base import ContentFile
from cad_pipeline.models.exported_file import ExportedFile
from cad_pipeline.cad_engine.globals.cache_manager import cache_exported_file


def export_assembly(assembly, file_name, export_formats=["step", "stl"], component=None):
    """
    Exports a CadQuery Workplane and stores the result in the database.
    """
    exported_files = {}

    for fmt in export_formats:
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{fmt}") as tmp_file:
                temp_path = tmp_file.name

            # ✅ Ensure Workplane objects are exported correctly
            if isinstance(assembly, cq.Workplane):
                cq.exporters.export(assembly, temp_path)
            else:
                raise TypeError(f"❌ Invalid object type: {type(assembly)}. Expected `Workplane`.")

            with open(temp_path, "rb") as file:
                file_data = file.read()

                # ✅ Save to database
                if component:
                    exported_file = ExportedFile.store_exported_file(component, fmt, file_data)
                    exported_files[fmt] = exported_file

                    # ✅ Cache exported file
                    cache_exported_file(exported_file)

        except Exception as e:
            raise RuntimeError(f"❌ Export failed for format {fmt}: {e}")

    return exported_files
