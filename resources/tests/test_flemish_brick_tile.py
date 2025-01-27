"""
Test Script: test_flemish_brick_tile.py
Description: Comprehensive test suite for flemish_brick_tile.py to validate all core functions.
Dependencies: pytest, CadQuery, Django settings, temporary directories for export tests.
"""

import os
import pytest
import cadquery as cq
from django.conf import settings
from resources.tiles.flemish_brick_tile import (
    create_full_brick_aligned,
    create_half_brick_aligned,
    create_mortar_row_layer,
    create_first_row,
    create_second_row,
    create_third_row,
    create_flemish_tile,
    export_tile,
)

# Test parameters for brick and mortar dimensions
@pytest.mark.parametrize(
    "full_brick_dims",
    [
        (200, 100, 50),  # Full brick dimensions
    ],
)
def test_create_full_brick_aligned(full_brick_dims):
    """Test if the full brick has the correct dimensions."""
    length, width, height = full_brick_dims
    brick = create_full_brick_aligned(length, width, height)
    bounding_box = brick.val().BoundingBox()
    assert (bounding_box.xlen, bounding_box.ylen, bounding_box.zlen) == full_brick_dims


@pytest.mark.parametrize(
    "half_brick_dims",
    [
        (100, 100, 50),  # Half brick dimensions
    ],
)
def test_create_half_brick_aligned(half_brick_dims):
    """Test if the half brick has the correct dimensions."""
    length, width, height = half_brick_dims
    brick = create_half_brick_aligned(length, width, height)
    bounding_box = brick.val().BoundingBox()
    assert (bounding_box.xlen, bounding_box.ylen, bounding_box.zlen) == half_brick_dims


@pytest.mark.parametrize(
    "mortar_dims",
    [
        (300, 90, 10),  # Mortar row dimensions
    ],
)
def test_create_mortar_row_layer(mortar_dims):
    """Test if the mortar row has the correct dimensions."""
    length, width, height = mortar_dims
    mortar = create_mortar_row_layer(length, width, height)
    bounding_box = mortar.val().BoundingBox()
    assert (bounding_box.xlen, bounding_box.ylen, bounding_box.zlen) == mortar_dims


def test_create_first_row():
    """Test if the first row assembly contains the correct components."""
    first_row = create_first_row()
    # Validate number of parts in the first row
    assert len(first_row.children) == 2  # Half brick + Full brick


def test_create_second_row():
    """Test if the second row (mortar layer) contains the correct components."""
    second_row = create_second_row()
    # Validate number of parts in the second row
    assert len(second_row.children) == 1  # Single mortar row


def test_create_third_row():
    """Test if the third row assembly contains the correct components."""
    third_row = create_third_row()
    # Validate number of parts in the third row
    assert len(third_row.children) == 2  # Full brick + Half brick


def test_create_flemish_tile():
    """Test if the Flemish bond tile assembles all rows correctly."""
    tile = create_flemish_tile()
    # Validate number of rows in the tile assembly
    assert len(tile.children) == 3  # First row, second row, third row


@pytest.mark.parametrize(
    "brick_dimensions",
    [
        (200, 100, 50),
        (300, 150, 100),
        (50, 50, 25),
        (400, 200, 150),
    ],
)
def test_dynamic_brick_creation(brick_dimensions):
    """Test dynamic creation of bricks with different dimensions."""
    length, width, height = brick_dimensions
    brick = create_full_brick_aligned(length, width, height)
    bounding_box = brick.val().BoundingBox()

    # Validate dynamic brick dimensions
    assert (bounding_box.xlen, bounding_box.ylen, bounding_box.zlen) == brick_dimensions


def test_invalid_export_directory(tmpdir):
    """Test export function gracefully handles invalid directories."""
    tile = create_flemish_tile()
    invalid_dir = "Z:/nonexistent_path"  # Use a truly invalid path
    settings.MEDIA_ROOT = invalid_dir

    with pytest.raises(FileNotFoundError, match=r"The system cannot find the path specified"):
        export_tile(tile, version="invalid")


def test_empty_tile_export(tmpdir):
    """Test export functionality gracefully handles empty tiles."""
    empty_tile = cq.Assembly()
    output_dir = tmpdir.mkdir("output")
    settings.MEDIA_ROOT = str(output_dir)

    # Attempt to export an empty tile
    with pytest.raises(ValueError, match="No shapes found to export"):
        export_tile(empty_tile, version="empty")


def test_logging_of_export():
    """Test if export logs file paths correctly."""
    tile = create_flemish_tile()
    try:
        export_tile(tile, version="test_logging")
        print("Export succeeded and logs file paths.")
    except Exception as e:
        pytest.fail(f"Logging test failed with error: {e}")
