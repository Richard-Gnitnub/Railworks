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
        config = yaml.safe_load(file)

    # Ensure tile_type exists
    if "tile_type" not in config:
        raise ValueError(f"Missing 'tile_type' key in {config_path}")

    return config


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
            "mortar_chamfer",
            "row_repetition", "tile_width", "export_formats",
        ],
        "plain_track": [
            "track_length", "track_width", "track_height",
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

def get_default_config_path(tile_type: str) -> str:
    """
    Retrieve the default configuration file path for the given tile type.
    :param tile_type: The type of tile (e.g., "brick_tile", "plain_track").
    :return: Path to the default configuration file.
    """
    base_dir = "resources/configs"
    file_paths = {
        "brick_tile": os.path.join(base_dir, "bricks/brick_tile.yaml"),  # Ensure correct naming
        "plain_track": os.path.join(base_dir, "tracks/plain_track.yaml"),
    }

    # Convert aliases (e.g., "bricks" → "brick_tile")
    tile_type_mappings = {
        "bricks": "brick_tile",  # Normalize to match the correct YAML file
        "plain_tracks": "plain_track",
    }

    # Convert if necessary
    normalized_type = tile_type_mappings.get(tile_type, tile_type)

    if normalized_type not in file_paths:
        raise ValueError(f"Unsupported tile type: {tile_type}")

    # Debugging: Print the resolved path
    print(f"Resolved config path: {file_paths[normalized_type]}")
    return file_paths[normalized_type]