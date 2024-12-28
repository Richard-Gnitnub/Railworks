import factory
from factory import Faker, Sequence, SubFactory
from factory.django import DjangoModelFactory
from trackbuilder_app.models import (
    Gauge,
    BullheadChairs,
    BullheadJawSection,
    BullheadKey,
    BullheadBossAndFerrule,
    Track,
    Timber,
    STLDownloadLog,
    UserProfile,
)
from django.contrib.auth.models import User


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = Sequence(lambda n: f"user_{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@example.com")


class UserProfileFactory(DjangoModelFactory):
    class Meta:
        model = UserProfile

    user = SubFactory(UserFactory)
    role = "user"


class GaugeFactory(DjangoModelFactory):
    class Meta:
        model = Gauge

    name = Sequence(lambda n: f"Gauge_{n}")
    width = factory.Faker("pyfloat", positive=True, min_value=0.0001, max_value=100)
    description = factory.Faker("sentence")


class BullheadChairsFactory(DjangoModelFactory):
    class Meta:
        model = BullheadChairs

    type = factory.Iterator(["S1", "L1", "SC"])
    plinth_thickness = factory.Faker("pyfloat", positive=True, min_value=0.0001, max_value=2)
    edge_thickness = factory.Faker("pyfloat", positive=True, min_value=0.0001, max_value=2)
    seat_thickness = factory.Faker("pyfloat", positive=True, min_value=0.0001, max_value=2)
    key_length = factory.Faker("pyfloat", positive=True, min_value=0.0001, max_value=5)
    key_deformation = factory.Faker("pyfloat", positive=True, min_value=0.0001, max_value=0.05)
    key_pad_taper = factory.Faker("pyfloat", positive=True, min_value=0.0001, max_value=0.1)
    boss_height = factory.Faker("pyfloat", positive=True, min_value=0.0001, max_value=1)
    ferrule_height = factory.Faker("pyfloat", positive=True, min_value=0.0001, max_value=1)
    bolt_head_height = factory.Faker("pyfloat", positive=True, min_value=0.0001, max_value=1)
    boss_diameter = factory.Faker("pyfloat", positive=True, min_value=0.0001, max_value=1)
    hole_diameter = factory.Faker("pyfloat", positive=True, min_value=0.0001, max_value=1)


class BullheadJawSectionFactory(DjangoModelFactory):
    class Meta:
        model = BullheadJawSection

    chair = SubFactory(BullheadChairsFactory)
    jaw_type = factory.Iterator(["outer", "inner"])
    section = factory.Iterator(["top", "mid", "seat", "plinth"])
    rib_depth = factory.Faker("pyfloat", positive=True, min_value=0.0001, max_value=1)
    rib_width = factory.Faker("pyfloat", positive=True, min_value=0.0001, max_value=1)
    rib_space = factory.Faker("pyfloat", positive=True, min_value=0.0001, max_value=1)
    rib_count = factory.Faker("pyint", min_value=1, max_value=5)
    half_width = factory.Faker("pyfloat", positive=True, min_value=0.0001, max_value=1)
    depth = factory.Faker("pyfloat", positive=True, min_value=0.0001, max_value=1)
    fillet_radius = factory.Faker("pyfloat", positive=True, min_value=0.0001, max_value=0.1)
    slope = factory.Faker("pyfloat", positive=True, min_value=0.0001, max_value=30)
    bolt_position = None


class BullheadKeyFactory(DjangoModelFactory):
    class Meta:
        model = BullheadKey

    chair = SubFactory(BullheadChairsFactory)
    type = factory.Iterator(["solid", "loose"])
    length = factory.Faker("pyfloat", positive=True, min_value=0.0001, max_value=5)
    pad_length = factory.Faker("pyfloat", positive=True, min_value=0.0001, max_value=1)
    deformation = factory.Faker("pyfloat", positive=True, min_value=0.0001, max_value=0.1)


class BullheadBossAndFerruleFactory(DjangoModelFactory):
    class Meta:
        model = BullheadBossAndFerrule

    chair = SubFactory(BullheadChairsFactory)
    component = factory.Iterator(["boss", "ferrule", "bolt"])
    height = factory.Faker("pyfloat", positive=True, min_value=0.0001, max_value=1)
    diameter = factory.Faker("pyfloat", positive=True, min_value=0.0001, max_value=1)


class TrackFactory(DjangoModelFactory):
    class Meta:
        model = Track

    gauge = SubFactory(GaugeFactory)
    chair_type = SubFactory(BullheadChairsFactory)  # Ensure chair_type is set
    total_length = factory.Faker("pyfloat", positive=True, min_value=0.0001, max_value=1000)
    timber_spacing = factory.Faker("pyfloat", positive=True, min_value=0.0001, max_value=10)
    chair_alignment = factory.Iterator(["opposite", "staggered"])
    is_straight = True
    kerf_adjustment = factory.Maybe(
        factory.Faker("pybool"),
        yes_declaration=None,
        no_declaration=factory.Faker("pyfloat", positive=True, min_value=0.0001, max_value=1),
    )
    flange_width = factory.Maybe(
        factory.Faker("pybool"),
        yes_declaration=None,
        no_declaration=factory.Faker("pyfloat", positive=True, min_value=0.0001, max_value=1),
    )
    flange_depth = factory.Maybe(
        factory.Faker("pybool"),
        yes_declaration=None,
        no_declaration=factory.Faker("pyfloat", positive=True, min_value=0.0001, max_value=1),
    )


class TimberFactory(DjangoModelFactory):
    class Meta:
        model = Timber

    track = SubFactory(TrackFactory)
    chair = SubFactory(BullheadChairsFactory)  # Add a valid chair instance
    length = factory.Faker("pyfloat", positive=True, min_value=0.0001, max_value=100)
    width = factory.Faker("pyfloat", positive=True, min_value=0.0001, max_value=10)
    depth = factory.Faker("pyfloat", positive=True, min_value=0.0001, max_value=10)
    position = factory.Faker("pyfloat", positive=True, min_value=0.0001, max_value=100)


class STLDownloadLogFactory(DjangoModelFactory):
    class Meta:
        model = STLDownloadLog

    user = SubFactory(UserFactory)
    chair = SubFactory(BullheadChairsFactory)
    track = SubFactory(TrackFactory)
    file_path = "path/to/file.stl"
