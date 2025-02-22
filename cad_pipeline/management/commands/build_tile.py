from django.core.management.base import BaseCommand
from cad_pipeline.generators.abstract_generator import generate_object
from ocp_vscode import show_object

class Command(BaseCommand):
    help = 'Builds an assembly using the design pattern generator.'

    def add_arguments(self, parser):
        parser.add_argument('assembly_name', type=str, help='Name of the assembly to generate')

    def handle(self, *args, **options):
        assembly_name = options['assembly_name']
        self.stdout.write(f"Generating assembly: {assembly_name}")
        generated_obj = generate_object(assembly_name)
        if generated_obj:
            show_object(generated_obj, name="Abstract Generated Object")
            self.stdout.write(self.style.SUCCESS(f"Successfully generated assembly '{assembly_name}'."))
        else:
            self.stdout.write(self.style.ERROR(f"Failed to generate assembly '{assembly_name}'."))
