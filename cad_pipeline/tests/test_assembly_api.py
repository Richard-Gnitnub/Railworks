import pytest
from django.core.cache import cache
from ninja import NinjaAPI
from ninja.testing import TestClient

# Create a fresh API instance and attach the assembly router.
# (This ensures that we do not reattach the router if it was attached elsewhere.)
from cad_pipeline.api.assembly_api import router as assembly_router
test_api = NinjaAPI()
test_api.add_router("", assembly_router)
client = TestClient(test_api)

from cad_pipeline.models.assembly import Assembly
from cad_pipeline.api.schemas.assembly_schema import AssemblySchema, ErrorResponse

# -------------------------------------------------------------------
# Fixtures
# -------------------------------------------------------------------
@pytest.fixture
def nmra_standard(db):
    from cad_pipeline.models.nmra_standard import NMRAStandard
    # Use a float for scale_ratio (e.g. 1/87 ≈ 0.01149) instead of a string.
    return NMRAStandard.objects.create(
        name="Test Standard",
        scale_ratio=1 / 87,
        gauge_mm=16.5,
        rail_profile="Profile1"
    )

@pytest.fixture
def assembly(db, nmra_standard):
    return Assembly.objects.create(
        name="Test Assembly",
        model_type="tile",
        nmra_standard=nmra_standard,
        metadata={"key": "value"},
        is_deleted=False,
        version=1,
    )

@pytest.fixture
def create_assembly(db, nmra_standard):
    return Assembly.objects.create(
        name="Test Assembly",
        model_type="tile",
        nmra_standard=nmra_standard,
        metadata={"key": "value"},
        is_deleted=False,
        version=1,
    )

# -------------------------------------------------------------------
# API Endpoint Tests
# -------------------------------------------------------------------
@pytest.mark.django_db
def test_get_assembly_success(assembly):
    """GET /assembly/{id}/ returns a non-deleted assembly (and caches it)."""
    response = client.get(f"/assembly/{assembly.id}/")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == assembly.id
    # Check that the assembly is cached
    assert cache.get(f"assembly:{assembly.id}") is not None

@pytest.mark.django_db
def test_get_assembly_soft_deleted(assembly):
    """GET /assembly/{id}/ returns 404 for a soft-deleted assembly."""
    assembly.is_deleted = True
    assembly.save(update_fields=["is_deleted"])
    response = client.get(f"/assembly/{assembly.id}/")
    assert response.status_code == 404
    data = response.json()
    assert "error" in data
    assert data["error"] == "This assembly has been deleted."

@pytest.mark.django_db
def test_get_assembly_not_found():
    """GET /assembly/999999/ returns 404 if no such assembly exists."""
    response = client.get("/assembly/999999/")
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data or "error" in data

@pytest.mark.django_db
def test_list_assemblies(assembly, nmra_standard):
    """GET /assemblies/ returns only non-deleted assemblies and supports filtering."""
    # Create a second (non-deleted) assembly.
    Assembly.objects.create(
        name="Another Assembly",
        model_type="Type B",
        nmra_standard=nmra_standard,
        metadata={"another": "info"},
        is_deleted=False,
        version=1,
    )
    # Create a soft-deleted assembly.
    Assembly.objects.create(
        name="Deleted Assembly",
        model_type="Type A",
        nmra_standard=nmra_standard,
        metadata={},
        is_deleted=True,
        version=1,
    )
    response = client.get("/assemblies/")
    assert response.status_code == 200
    data = response.json()
    # Only non-deleted assemblies should be returned.
    assert len(data) == 2

    # Test filtering by model_type.
    response = client.get("/assemblies/", params={"model_type": "Type A"})
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["model_type"] == "Type A"

@pytest.mark.django_db
def test_list_assemblies_no_match(nmra_standard):
    """GET /assemblies/ with a filter that matches nothing returns an empty list."""
    Assembly.objects.create(
        name="Assembly 1",
        model_type="Type X",
        nmra_standard=nmra_standard,
        metadata={},
        is_deleted=False,
        version=1,
    )
    response = client.get("/assemblies/", params={"model_type": "Non Existent"})
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 0

@pytest.mark.django_db
def test_create_assembly_success(nmra_standard):
    """POST /assemblies/ creates a new assembly and caches it."""
    payload = {
        "name": "New Assembly",
        "model_type": "Type C",
        "nmra_standard": nmra_standard.id,
        "metadata": {"info": "new"},
    }
    response = client.post("/assemblies/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "New Assembly"
    assembly_id = data["id"]
    # Verify the new assembly is cached.
    assert cache.get(f"assembly:{assembly_id}") is not None

@pytest.mark.django_db
def test_create_assembly_duplicate(nmra_standard):
    """POST /assemblies/ fails if an assembly with the same name already exists (non-deleted)."""
    Assembly.objects.create(
        name="Duplicate Assembly",
        model_type="Type D",
        nmra_standard=nmra_standard,
        metadata={},
        is_deleted=False,
        version=1,
    )
    payload = {
        "name": "Duplicate Assembly",
        "model_type": "Type D",
        "nmra_standard": nmra_standard.id,
        "metadata": {},
    }
    response = client.post("/assemblies/", json=payload)
    assert response.status_code == 400
    data = response.json()
    assert "error" in data
    assert data["error"] == "An assembly with this name already exists."

@pytest.mark.django_db
def test_update_assembly_success(assembly):
    """PUT /assembly/{id}/ updates an assembly. The model’s save() handles versioning and cache update."""
    payload = {
        "name": "Updated Assembly",
        "model_type": assembly.model_type,
        "metadata": {"new_key": "new_value"},
    }
    response = client.put(f"/assembly/{assembly.id}/", json=payload)
    assert response.status_code == 200
    assembly.refresh_from_db()
    assert assembly.name == "Updated Assembly"
    # Verify cache is updated.
    cached = cache.get(f"assembly:{assembly.id}")
    assert cached is not None
    assert cached.name == "Updated Assembly"

@pytest.mark.django_db
def test_update_assembly_no_metadata_change(assembly):
    """PUT /assembly/{id}/ updates fields without changing metadata; version remains unchanged."""
    original_version = assembly.version
    payload = {"name": "Updated Assembly No Meta"}
    response = client.put(f"/assembly/{assembly.id}/", json=payload)
    assert response.status_code == 200
    assembly.refresh_from_db()
    assert assembly.version == original_version
    assert assembly.name == "Updated Assembly No Meta"

@pytest.mark.django_db
def test_update_assembly_soft_deleted(assembly):
    """PUT /assembly/{id}/ returns 404 when attempting to update a soft-deleted assembly."""
    assembly.is_deleted = True
    assembly.save(update_fields=["is_deleted"])
    payload = {"name": "Should Not Update"}
    response = client.put(f"/assembly/{assembly.id}/", json=payload)
    assert response.status_code == 404
    data = response.json()
    assert "error" in data
    assert data["error"] == "This assembly has been deleted."

@pytest.mark.django_db
def test_delete_assembly_success(assembly):
    """DELETE /assembly/{id}/ performs a soft delete and invalidates the cache."""
    response = client.delete(f"/assembly/{assembly.id}/")
    assert response.status_code == 204
    assembly.refresh_from_db()
    assert assembly.is_deleted is True
    # Verify GET returns 404 after deletion.
    response = client.get(f"/assembly/{assembly.id}/")
    assert response.status_code == 404

@pytest.mark.django_db
def test_delete_assembly_already_deleted(assembly):
    """DELETE /assembly/{id}/ returns 404 if the assembly is already soft-deleted."""
    assembly.is_deleted = True
    assembly.save(update_fields=["is_deleted"])
    response = client.delete(f"/assembly/{assembly.id}/")
    assert response.status_code == 404
    data = response.json()
    assert "error" in data
    assert data["error"] == "This assembly has already been deleted."

# -------------------------------------------------------------------
# Model and Caching Tests (Directly on the Model)
# -------------------------------------------------------------------
@pytest.mark.django_db
def test_update_or_create(nmra_standard):
    """Test update_or_create_with_version creates or updates an assembly.
    Version incrementation is handled by the model's save() method."""
    assembly = Assembly.update_or_create_with_version(
        name="Test Assembly",
        model_type="wall",
        metadata={"height": 300, "width": 500},
    )
    assert assembly.name == "Test Assembly"

@pytest.mark.django_db
def test_update_assembly_metadata(create_assembly):
    """Test that update_or_create_with_version updates metadata and
    that save() handles version incrementation when metadata changes.
    (Here we expect the version to increment by 1.)"""
    # First, force a cache hit.
    _ = Assembly.get_cached_assembly(create_assembly.id)
    updated_assembly = Assembly.update_or_create_with_version(
        name="Test Assembly",
        model_type=create_assembly.model_type,
        metadata={"brick_length": 250, "brick_width": 120},
    )
    # Expect version to increment if metadata has changed.
    assert updated_assembly.version == create_assembly.version + 1

@pytest.mark.django_db
def test_cache_behavior_on_update(create_assembly):
    """Test that updating an assembly updates the cached instance's metadata."""
    cache_key = f"assembly:{create_assembly.id}"
    _ = Assembly.get_cached_assembly(create_assembly.id)
    cached_before = cache.get(cache_key)
    assert cached_before is not None
    # Update metadata and save.
    create_assembly.metadata = {"brick_length": 300, "brick_width": 150}
    create_assembly.save()
    updated_cached = cache.get(cache_key)
    # Verify that the cached object's metadata reflects the update.
    assert updated_cached is not None
    assert updated_cached.metadata == {"brick_length": 300, "brick_width": 150}

@pytest.mark.django_db
def test_version_increment_on_metadata_change(create_assembly):
    """Test that when metadata changes, the model's save() increments the version.
    (If your business logic does not increment, adjust accordingly.)"""
    # Force caching so that the save() method can compare.
    _ = Assembly.get_cached_assembly(create_assembly.id)
    initial_version = create_assembly.version
    create_assembly.metadata = {"new_key": "new_value"}
    create_assembly.save()
    create_assembly.refresh_from_db()
    # In this consolidated design, we expect the version to increment.
    assert create_assembly.version == initial_version + 1

@pytest.mark.django_db
def test_soft_delete(create_assembly):
    """Test that delete() performs a soft delete and that a subsequent GET returns 404."""
    create_assembly.delete()
    response = client.get(f"/assembly/{create_assembly.id}/")
    assert response.status_code == 404

@pytest.mark.django_db
def test_update_or_create_method(nmra_standard):
    """Another test for update_or_create_with_version to ensure it returns the updated assembly."""
    updated_assembly = Assembly.update_or_create_with_version(
        name="Test Assembly",
        model_type="wall",
        metadata={"brick_length": 300, "brick_width": 200},
    )
    assert updated_assembly.name == "Test Assembly"
