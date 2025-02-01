import yaml
import os

def load_config(config_path="cad_pipeline/configs/config_v2.yaml"):
    """
    Load configuration from a YAML file.
    :param config_path: Path to the YAML configuration file.
    :return: Dictionary containing the configuration.
    """
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    with open(config_path, "r") as file:
        return yaml.safe_load(file)

def validate_config(config):
    """
    Validate the loaded configuration for required keys.
    :param config: Dictionary containing the configuration.
    :raises ValueError: If a required key is missing.
    """
    required_keys = [
        "brick_length", "brick_width", "brick_height",
        "mortar_chamfer",  # Ensure chamfer is validated
        "offset_x", "offset_y", "row_repetition", "tile_width", "export_formats",
    ]
    for key in required_keys:
        if key not in config:
            raise ValueError(f"Missing required configuration key: {key}")


