from resources.configs.yaml_config import load_config, validate_config

# Load and validate the configuration
config = load_config("resources/configs/default_config_v2.yaml")
validate_config(config)

# Print for verification
print("Config loaded and validated successfully:", config)
