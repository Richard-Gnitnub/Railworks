# generators/generator_strategy.py

class IGenerator:
    def generate(self, assembly):
        """
        Generate the CAD output for the given assembly.
        
        Parameters:
            assembly (Assembly): An object representing the assembly details.
            
        Raises:
            NotImplementedError: Must be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses must implement the generate method")
