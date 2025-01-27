import os
import pytest
from django.conf import settings
import cadquery as cq
from tiles.flemish_brick_tile import (
    create_full_brick_aligned,
    create_half_brick_aligned,
    create_mortar_row_layer,
    create_first_row,
    create_second_row,
    create_third_row,
    create_flemish_tile,
    export_tile,
)

# Test parameters
@pytest.mark.parametrize("expected_dims", [(200, 100, 50)])
def test_create_full_brick_aligned(expected_dims):
    """Test if the full brick has the correct dimensions."""
    brick = create_full_brick_aligned()
    bounding_box = brick.val().BoundingBox()
    assert (bounding_box.xlen, bounding_box.ylen, bounding_box.zlen) == expected_dims


@pytest.mark.parametrize("expected_dims", [(100, 100, 50)])
def test_create_half_brick_aligned(expected_dims):
    """Test if the half brick has the correct dimensions."""
    brick = create_half_brick_aligned()
    bounding_box = brick.val().BoundingBox()
    assert (bounding_box.xlen, bounding_box.ylen, bounding_box.zlen) == expected_dims


@pytest.mark.parametrize("expected_dims", [(300, 90, 10)])
def test_create_mortar_row_layer(expected_dims):
    """Test if the mortar row has the correct dimensions."""
    mortar = create_mortar_row_layer()
    bounding_box = mortar.val().BoundingBox()
    assert (bounding_box.xlen, bounding_box.ylen, bounding_box.zlen) == expected_dims


def test_create_first_row():
    """Test if the first row assembly has the correct number of parts."""
    first_row = create_first_row()
    assert len(first_row.children) == 2  # Half brick + Full brick


def test_create_second_row():
    """Test if the second row (mortar layer) has the correct number of parts."""
    second_row = create_second_row()
    assert len(second_row.children) == 1  # Mortar row


def test_create_third_row():
    """Test if the third row assembly has the correct number of parts."""
    third_row = create_third_row()
    assert len(third_row.children) == 2  # Full brick + Half brick


def test_create_flemish_tile():
    """Test if the Flemish bond tile assembles correctly."""
    tile = create_flemish_tile()
    assert len(tile.children) == 3  # First row, second row, third row


def test_export_tile(tmpdir):
    """Test if STEP and STL files are exported correctly."""
    tile = create_flemish_tile()
    output_dir = tmpdir.mkdir("output")
    os.environ["DJANGO_SETTINGS_MODULE"] = "railworks_project.settings"

    # Create dummy media root
    settings.MEDIA_ROOT = str(output_dir)

    # Run export
    try:
        export_tile(tile, version="test")
        step_file = os.path.join(output_dir, "resources", "tiles", "vtest", "flemish_tile_test.step")
        stl_file = os.path.join(output_dir, "resources", "tiles", "vtest", "flemish_tile_test.stl")
        assert os.path.exists(step_file)
        assert os.path.exists(stl_file)
    except Exception as e:
        pytest.fail(f"Export failed with error: {e}")
