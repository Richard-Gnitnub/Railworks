import pytest
from django.core.cache import cache
from cad_pipeline.models import Assembly


@pytest.fixture
def create_assembly():
    """Fixture to create a sample assembly."""
    return Assembly.objects.create(
        name="Test Assembly",
        model_type="tile",
        metadata={"brick_length": 200, "brick_width": 100},
    )


def test_create_assembly(db):
    """Test creating a new assembly."""
    assembly, created = Assembly.update_or_create_with_version(
        name="New Assembly",
        defaults={
            "model_type": "wall",
            "metadata": {"height": 300, "width": 500},
        },
    )
    assert created is True
    assert assembly.name == "New Assembly"
    assert assembly.version == 1
    assert assembly.metadata == {"height": 300, "width": 500}


def test_update_assembly_metadata(db, create_assembly):
    """Test updating an assembly's metadata and version."""
    updated_assembly, created = Assembly.update_or_create_with_version(
        name="Test Assembly",
        defaults={
            "metadata": {"brick_length": 250, "brick_width": 120},
        },
    )
    assert created is False
    assert updated_assembly.version == 2  # Version should increment
    assert updated_assembly.metadata == {"brick_length": 250, "brick_width": 120}


def test_cache_behavior_on_create(db, create_assembly):
    """Test that new assemblies are cached properly."""
    cache_key = f"assembly:{create_assembly.id}"
    assert cache.get(cache_key) is None

    # Trigger caching by calling the helper method
    Assembly.get_cached_assembly(create_assembly.id)
    cached_assembly = cache.get(cache_key)
    assert cached_assembly is not None
    assert cached_assembly.name == "Test Assembly"


def test_cache_behavior_on_update(db, create_assembly):
    """Test cache updates when an assembly is modified."""
    cache_key = f"assembly:{create_assembly.id}"
    Assembly.get_cached_assembly(create_assembly.id)  # Populate the cache
    assert cache.get(cache_key) is not None

    # Update the assembly and ensure cache is cleared
    create_assembly.metadata = {"brick_length": 300, "brick_width": 150}
    create_assembly.save()
    assert cache.get(cache_key) is None  # Cache should be cleared

    # Repopulate cache with updated data
    cached_assembly = Assembly.get_cached_assembly(create_assembly.id)
    assert cached_assembly.metadata == {"brick_length": 300, "brick_width": 150}


def test_soft_delete(db, create_assembly):
    """Test soft deletion of an assembly."""
    create_assembly.delete()
    assert create_assembly.is_deleted is True

    # Ensure soft-deleted assemblies are not served from the cache
    cache_key = f"assembly:{create_assembly.id}"
    Assembly.get_cached_assembly(create_assembly.id)
    cached_assembly = cache.get(cache_key)
    assert cached_assembly is None


def test_version_retention_on_non_metadata_updates(db, create_assembly):
    """Ensure version does not change if metadata is not modified."""
    initial_version = create_assembly.version
    create_assembly.name = "Renamed Assembly"
    create_assembly.save()
    assert create_assembly.version == initial_version  # Version should remain unchanged


def test_version_increment_on_metadata_change(db, create_assembly):
    """Ensure version increments on metadata modification."""
    initial_version = create_assembly.version
    create_assembly.metadata = {"new_key": "new_value"}
    create_assembly.save()
    assert create_assembly.version == initial_version + 1


def test_update_or_create(db):
    """Test the update_or_create_with_version method."""
    assembly, created = Assembly.update_or_create_with_version(
        name="Test Assembly",
        defaults={
            "metadata": {"brick_length": 300, "brick_width": 200},
        },
    )
    assert created is False
    assert assembly.version == 2  # Version should increment
    assert assembly.metadata == {"brick_length": 300, "brick_width": 200}
