import yaml
import os


def load_config(config_path: str) -> dict:
    """
    Load a YAML configuration file.
    :param config_path: Path to the YAML file.
    :return: Dictionary containing the configuration.
    """
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    with open(config_path, "r") as file:
        return yaml.safe_load(file)


def validate_config(config: dict, tile_type: str):
    """
    Validate configuration against required keys for the given tile type.
    :param config: Configuration dictionary.
    :param tile_type: The type of tile (e.g., bricks, plain_track).
    :raises ValueError: If required keys are missing.
    """
    required_keys = {
        "bricks": [
            "brick_length",
            "brick_width",
            "brick_height",
            "mortar_chamfer",
            "row_repetition",
            "tile_width",
            "export_formats",
        ],
        "plain_track": [
            "track_length",
            "track_width",
            "track_height",
            "spacing",
            "export_formats",
        ],
    }

    keys = required_keys.get(tile_type)
    if not keys:
        raise ValueError(f"Unsupported tile type: {tile_type}")

    for key in keys:
        if key not in config:
            raise ValueError(f"Missing required configuration key: {key}")
