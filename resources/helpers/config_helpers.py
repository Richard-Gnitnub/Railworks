"""
config_helpers.py - Handles loading and validating YAML configurations for different tile types.
"""

import yaml
import os


def load_config(config_path: str) -> dict:
    """
    Load configuration from a YAML file.
    :param config_path: Path to the YAML configuration file.
    :return: Dictionary containing the configuration.
    """
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    with open(config_path, "r") as file:
        return yaml.safe_load(file)


def validate_config(config: dict, tile_type: str):
    """
    Validate the loaded configuration for required keys based on the tile type.
    :param config: Dictionary containing the configuration.
    :param tile_type: The type of tile (e.g., "bricks", "plain_track").
    :raises ValueError: If a required key is missing.
    """
    required_keys = {
        "bricks": [
            "brick_length", "brick_width", "brick_height",
            "mortar_chamfer",  # Ensure chamfer is validated
            "row_repetition", "tile_width", "export_formats",
        ],
        "plain_track": [
            "track_length", "track_width", "track_height",
            "spacing",  # Spacing between sleepers
            "export_formats",
        ],
    }

    # Retrieve the required keys for the specified tile type
    keys = required_keys.get(tile_type)
    if not keys:
        raise ValueError(f"Unsupported tile type: {tile_type}")

    # Validate all required keys are present
    for key in keys:
        if key not in config:
            raise ValueError(f"Missing required configuration key: {key}")


def list_supported_tile_types() -> list:
    """
    Return a list of supported tile types for validation.
    :return: List of supported tile types.
    """
    return ["bricks", "plain_track"]


def get_default_config_path(tile_type: str) -> str:
    """
    Retrieve the default configuration file path for the given tile type.
    :param tile_type: The type of tile (e.g., "bricks", "plain_track").
    :return: Path to the default configuration file.
    """
    base_dir = "resources/configs"
    file_paths = {
        "bricks": os.path.join(base_dir, "bricks/flemish_brick_tile.yaml"),
        "plain_track": os.path.join(base_dir, "tracks/plain_track.yaml"),
    }

    if tile_type not in file_paths:
        raise ValueError(f"Unsupported tile type: {tile_type}")

    return file_paths[tile_type]
