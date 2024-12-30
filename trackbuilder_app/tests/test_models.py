import pytest
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from trackbuilder_app.models import (
    Gauge,
    BullheadChairs,
    BullheadJawSection,
    BullheadKey,
    BullheadBossAndFerrule,
    Track,
    Timber,
    UserProfile,
    STLDownloadLog,
)
from .factories import (
    GaugeFactory,
    BullheadChairsFactory,
    BullheadJawSectionFactory,
    BullheadKeyFactory,
    BullheadBossAndFerruleFactory,
    TrackFactory,
    TimberFactory,
    UserProfileFactory,
    STLDownloadLogFactory,
)


@pytest.mark.django_db
class TestGauge:
    def test_create(self):
        gauge = GaugeFactory()
        assert gauge.pk is not None
        assert isinstance(gauge, Gauge)

    def test_str_method(self):
        gauge = GaugeFactory(name="Test Gauge")
        assert str(gauge) == "Test Gauge"

    def test_unique_constraint(self):
        gauge_name = "UniqueGauge"
        GaugeFactory(name=gauge_name)
        with pytest.raises(IntegrityError):
            GaugeFactory(name=gauge_name)

    def test_null_description(self):
        gauge = GaugeFactory(description=None)
        assert gauge.description is None


@pytest.mark.django_db
class TestBullheadChairs:
    def test_create(self):
        chair = BullheadChairsFactory()
        assert chair.pk is not None
        assert isinstance(chair, BullheadChairs)

    def test_str_method(self):
        chair = BullheadChairsFactory(type="S1")
        assert str(chair) == "S1"

    def test_invalid_choice(self):
        # Build only and then validate
        chair = BullheadChairsFactory.build(type="INVALID")
        with pytest.raises(ValidationError):
            chair.full_clean()

    def test_negative_measurement(self):
        # Some fields likely shouldn’t be negative
        chair = BullheadChairsFactory.build(plinth_thickness=-0.5)
        with pytest.raises(ValidationError):
            chair.full_clean()


@pytest.mark.django_db
class TestBullheadJawSection:
    def test_create(self):
        jaw_section = BullheadJawSectionFactory()
        assert jaw_section.pk is not None
        assert isinstance(jaw_section, BullheadJawSection)

    def test_str_method(self):
        jaw_section = BullheadJawSectionFactory(jaw_type="outer", section="top")
        assert str(jaw_section) == "Outer Top Section"

    def test_invalid_jaw_type_choice(self):
        jaw_section = BullheadJawSectionFactory.build(jaw_type="INVALID")
        with pytest.raises(ValidationError):
            jaw_section.full_clean()

    def test_invalid_section_choice(self):
        jaw_section = BullheadJawSectionFactory.build(section="INVALID")
        with pytest.raises(ValidationError):
            jaw_section.full_clean()

    def test_allows_null_bolt_position(self):
        jaw_section = BullheadJawSectionFactory(bolt_position=None)
        assert jaw_section.bolt_position is None


@pytest.mark.django_db
class TestBullheadKey:
    def test_create(self):
        key = BullheadKeyFactory()
        assert key.pk is not None
        assert isinstance(key, BullheadKey)

    def test_str_method(self):
        key = BullheadKeyFactory(type="solid")
        assert str(key) == "Solid Key"

    def test_invalid_type_choice(self):
        key = BullheadKeyFactory.build(type="INVALID")
        with pytest.raises(ValidationError):
            key.full_clean()


@pytest.mark.django_db
class TestBullheadBossAndFerrule:
    def test_create(self):
        component = BullheadBossAndFerruleFactory()
        assert component.pk is not None
        assert isinstance(component, BullheadBossAndFerrule)

    def test_str_method(self):
        component = BullheadBossAndFerruleFactory(component="boss")
        assert str(component) == "Boss"

    def test_invalid_component_choice(self):
        component = BullheadBossAndFerruleFactory.build(component="INVALID")
        with pytest.raises(ValidationError):
            component.full_clean()


@pytest.mark.django_db
class TestTrack:
    def test_create(self):
        track = TrackFactory()
        assert track.pk is not None
        assert isinstance(track, Track)

    def test_str_method(self):
        track = TrackFactory()
        assert str(track) == f"Track {track.id}"

    def test_null_fields(self):
        track = TrackFactory(kerf_adjustment=None, flange_width=None, flange_depth=None)
        assert track.kerf_adjustment is None
        assert track.flange_width is None
        assert track.flange_depth is None

    def test_invalid_choice_alignment(self):
        track = TrackFactory.build(chair_alignment="INVALID")
        with pytest.raises(ValidationError):
            track.full_clean()

    def test_relationship_to_gauge_and_chair(self):
        track = TrackFactory()
        assert track.gauge is not None
        assert track.chair_type is not None


@pytest.mark.django_db
class TestTimber:
    def test_create(self):
        timber = TimberFactory()
        assert timber.pk is not None
        assert isinstance(timber, Timber)

    def test_str_method(self):
        timber = TimberFactory()
        assert str(timber) == f"Timber {timber.id} for Track {timber.track.id}"

    def test_relationship_to_track_and_chair(self):
        timber = TimberFactory()
        assert timber.track is not None
        assert timber.chair is not None

    def test_negative_position(self):
        timber = TimberFactory.build(position=-10.0)
        # Depending on your app’s logic, negative might be okay or not
        # If it's not okay, you'd do:
        with pytest.raises(ValidationError):
            timber.full_clean()

    def test_unusually_large_dimensions(self):
        # This may or may not be invalid, depending on your real constraints
        timber = TimberFactory.build(length=999999999)
        # If your model doesn’t allow such large values, full_clean should fail
        with pytest.raises(ValidationError):
            timber.full_clean()


@pytest.mark.django_db
class TestUserProfile:
    def test_create(self):
        profile = UserProfileFactory()
        assert profile.pk is not None
        assert isinstance(profile, UserProfile)

    def test_str_method(self):
        profile = UserProfileFactory(role="user")
        assert str(profile) == f"{profile.user.username} - User"

    def test_invalid_role_choice(self):
        profile = UserProfileFactory.build(role="INVALID")
        with pytest.raises(ValidationError):
            profile.full_clean()

    def test_relationship_to_user(self):
        profile = UserProfileFactory()
        assert profile.user is not None


@pytest.mark.django_db
class TestSTLDownloadLog:
    def test_create(self):
        log = STLDownloadLogFactory()
        assert log.pk is not None
        assert isinstance(log, STLDownloadLog)

    def test_str_method(self):
        log = STLDownloadLogFactory()
        # Example: "username downloaded path/to/file.stl on 2024-01-01 12:00:00"
        assert log.user.username in str(log)
        assert log.file_path in str(log)

    def test_allow_null_chair_and_track(self):
        log = STLDownloadLogFactory(chair=None, track=None)
        assert log.chair is None
        assert log.track is None

    def test_long_file_path(self):
        long_path = "x" * 255
        log = STLDownloadLogFactory(file_path=long_path)
        assert len(log.file_path) == 255

    def test_relationship_to_user(self):
        log = STLDownloadLogFactory()
        assert log.user is not None
