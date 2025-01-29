"""
Test Script: test_flemish_brick_tile.py
Description: Test suite for flemish_brick_tile.py to validate YAML configuration integration, geometry generation, and exports.
"""

import os
import pytest
import cadquery as cq
from django.conf import settings
from resources.tiles.bricks.flemish_brick import (
    load_config,
    validate_config,
    create_full_brick_aligned,
    create_half_brick_aligned,
    create_mortar_row_layer,
    create_flemish_tile,
    export_tile,
)


# Test parameters for YAML configuration
@pytest.fixture
def valid_config(tmpdir):
    """Fixture to create a valid YAML configuration."""
    config_file = tmpdir.join("test_config.yaml")
    config_file.write(
        """
        brick_length: 250
        brick_width: 120
        brick_height: 60
        mortar_length: 300
        mortar_width: 90
        mortar_height: 15
        """
    )
    return str(config_file)


@pytest.fixture
def invalid_config(tmpdir):
    """Fixture to create an invalid YAML configuration."""
    config_file = tmpdir.join("invalid_config.yaml")
    config_file.write(
        """
        brick_length: 250
        brick_width: 120
        # Missing brick_height
        mortar_length: 300
        mortar_width: 90
        mortar_height: 15
        """
    )
    return str(config_file)


# Test loading and validation of YAML configurations
def test_load_config(valid_config):
    """Test loading a valid YAML configuration."""
    config = load_config(valid_config)
    assert config["brick_length"] == 250
    assert config["brick_width"] == 120
    assert config["brick_height"] == 60


def test_validate_config(valid_config):
    """Test validating a correct configuration."""
    config = load_config(valid_config)
    validate_config(config)  # Should pass without raising an exception


def test_validate_config_missing_key(invalid_config):
    """Test validating a configuration with missing keys."""
    config = load_config(invalid_config)
    with pytest.raises(ValueError, match="Missing required configuration key: brick_height"):
        validate_config(config)


# Test geometry creation
@pytest.mark.parametrize(
    "brick_dimensions",
    [
        (200, 100, 50),
        (300, 150, 100),
        (50, 50, 25),
        (400, 200, 150),
    ],
)
def test_create_full_brick_aligned(brick_dimensions):
    """Test full brick creation with parameterized dimensions."""
    length, width, height = brick_dimensions
    brick = create_full_brick_aligned(length, width, height)
    bounding_box = brick.val().BoundingBox()
    assert (bounding_box.xlen, bounding_box.ylen, bounding_box.zlen) == brick_dimensions


@pytest.mark.parametrize(
    "half_brick_dimensions",
    [
        (100, 100, 50),
        (150, 80, 60),
        (25, 25, 15),
    ],
)
def test_create_half_brick_aligned(half_brick_dimensions):
    """Test half brick creation with parameterized dimensions."""
    length, width, height = half_brick_dimensions
    brick = create_half_brick_aligned(length, width, height)
    bounding_box = brick.val().BoundingBox()
    assert (bounding_box.xlen, bounding_box.ylen, bounding_box.zlen) == half_brick_dimensions


@pytest.mark.parametrize(
    "mortar_dimensions",
    [
        (300, 90, 10),
        (500, 120, 15),
        (200, 70, 5),
    ],
)
def test_create_mortar_row_layer(mortar_dimensions):
    """Test mortar row creation with parameterized dimensions."""
    length, width, height = mortar_dimensions
    mortar = create_mortar_row_layer(length, width, height)
    bounding_box = mortar.val().BoundingBox()
    assert (bounding_box.xlen, bounding_box.ylen, bounding_box.zlen) == mortar_dimensions


def test_create_flemish_tile():
    """Test if the Flemish bond tile assembles all rows correctly."""
    tile = create_flemish_tile()
    assert len(tile.children) == 3  # Ensure all rows are included


# Test export functionality
def test_export_tile_with_yaml_config(valid_config, tmpdir):
    """Test export functionality with YAML-configured dimensions."""
    config = load_config(valid_config)
    tile = create_flemish_tile()

    output_dir = tmpdir.mkdir("output")
    os.environ["DJANGO_SETTINGS_MODULE"] = "railworks_project.settings"
    settings.MEDIA_ROOT = str(output_dir)

    export_tile(tile, version="yaml_test")
    step_file = os.path.join(output_dir, "resources", "tiles", "vyaml_test", "flemish_tile_yaml_test.step")
    stl_file = os.path.join(output_dir, "resources", "tiles", "vyaml_test", "flemish_tile_yaml_test.stl")

    # Ensure files were created
    assert os.path.exists(step_file)
    assert os.path.exists(stl_file)


def test_invalid_export_directory(tmpdir):
    """Test export function gracefully handles invalid directories."""
    tile = create_flemish_tile()
    invalid_dir = "Z:/nonexistent_path"  # Use a truly invalid path
    settings.MEDIA_ROOT = invalid_dir

    with pytest.raises(Exception, match=r"The system cannot find the path specified"):
        export_tile(tile, version="invalid")


def test_empty_tile_export(tmpdir):
    """Test export functionality gracefully handles empty tiles."""
    empty_tile = cq.Assembly()
    output_dir = tmpdir.mkdir("output")
    settings.MEDIA_ROOT = str(output_dir)

    # Attempt to export an empty tile
    with pytest.raises(ValueError, match="No shapes found to export"):
        export_tile(empty_tile, version="empty")
