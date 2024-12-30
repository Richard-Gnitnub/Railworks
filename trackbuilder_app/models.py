from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError


# Gauge Table
class Gauge(models.Model):
    name = models.CharField(max_length=50, unique=True)
    width = models.FloatField(help_text="Gauge width in mm")
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


# Bullhead Chair Table
class BullheadChairs(models.Model):
    CHAIR_TYPE_CHOICES = [
        ("S1", "Standard 1"),
        ("L1", "Large 1"),
        ("SC", "Special Chair"),
    ]

    type = models.CharField(
        max_length=50,
        choices=CHAIR_TYPE_CHOICES,
        help_text="Type of the chair",
    )
    plinth_thickness = models.FloatField(
        help_text="Plinth thickness in inches",
        validators=[MinValueValidator(0.0)],
    )
    edge_thickness = models.FloatField(
        help_text="Edge thickness in inches",
        validators=[MinValueValidator(0.0)],
    )
    seat_thickness = models.FloatField(
        help_text="Seat thickness under the rail in inches",
        validators=[MinValueValidator(0.0)],
    )
    key_length = models.FloatField(
        help_text="Length of the rail keys in inches",
        validators=[MinValueValidator(0.0)],
    )
    key_deformation = models.FloatField(
        help_text="Deformation factor for key fitting",
        validators=[MinValueValidator(0.0)],
    )
    key_pad_taper = models.FloatField(
        help_text="Taper of the key pad",
        validators=[MinValueValidator(0.0)],
    )
    boss_height = models.FloatField(
        help_text="Height of the boss in inches",
        validators=[MinValueValidator(0.0)],
    )
    ferrule_height = models.FloatField(
        help_text="Height of the ferrule in inches",
        validators=[MinValueValidator(0.0)],
    )
    bolt_head_height = models.FloatField(
        help_text="Height of the bolt head in inches",
        validators=[MinValueValidator(0.0)],
    )
    boss_diameter = models.FloatField(
        help_text="Diameter of the boss in inches",
        validators=[MinValueValidator(0.0)],
    )
    hole_diameter = models.FloatField(
        help_text="Diameter of the ferrule or hole in inches",
        validators=[MinValueValidator(0.0)],
    )

    def __str__(self):
        return self.type

    def clean(self):
        super().clean()
        if self.plinth_thickness > 10.0:
            raise ValidationError({
                "plinth_thickness": "Plinth thickness cannot exceed 10 inches."
            })


# Bullhead Jaw Section Table
class BullheadJawSection(models.Model):
    JAW_TYPE_CHOICES = [
        ("outer", "Outer"),
        ("inner", "Inner"),
    ]
    SECTION_TYPE_CHOICES = [
        ("top", "Top"),
        ("mid", "Middle"),
        ("seat", "Seat"),
        ("plinth", "Plinth"),
    ]

    chair = models.ForeignKey(
        BullheadChairs, on_delete=models.CASCADE, related_name="jaw_sections"
    )
    jaw_type = models.CharField(max_length=10, choices=JAW_TYPE_CHOICES)
    section = models.CharField(max_length=10, choices=SECTION_TYPE_CHOICES)
    rib_depth = models.FloatField()
    rib_width = models.FloatField()
    rib_space = models.FloatField()
    rib_count = models.IntegerField()
    half_width = models.FloatField()
    depth = models.FloatField()
    fillet_radius = models.FloatField()
    slope = models.FloatField()
    bolt_position = models.FloatField(blank=True, null=True)

    def __str__(self):
        return f"{self.jaw_type.capitalize()} {self.section.capitalize()} Section"


# Bullhead Key Table
class BullheadKey(models.Model):
    KEY_TYPE_CHOICES = [
        ("solid", "Solid"),
        ("loose", "Loose"),
    ]

    chair = models.ForeignKey(
        BullheadChairs, on_delete=models.CASCADE, related_name="keys"
    )
    type = models.CharField(max_length=10, choices=KEY_TYPE_CHOICES)
    length = models.FloatField()
    pad_length = models.FloatField()
    deformation = models.FloatField()

    def __str__(self):
        return f"{self.type.capitalize()} Key"


# Bullhead Boss and Ferrule Table
class BullheadBossAndFerrule(models.Model):
    COMPONENT_TYPE_CHOICES = [
        ("boss", "Boss"),
        ("ferrule", "Ferrule"),
        ("bolt", "Bolt"),
    ]

    chair = models.ForeignKey(
        BullheadChairs, on_delete=models.CASCADE, related_name="components"
    )
    component = models.CharField(max_length=10, choices=COMPONENT_TYPE_CHOICES)
    height = models.FloatField()
    diameter = models.FloatField(blank=True, null=True)

    def __str__(self):
        return f"{self.component.capitalize()}"


# Track Table
class Track(models.Model):
    CHAIR_ALIGNMENT_CHOICES = [
        ("opposite", "Opposite"),
        ("staggered", "Staggered"),
    ]

    gauge = models.ForeignKey(
        Gauge, on_delete=models.CASCADE, related_name="tracks"
    )
    total_length = models.FloatField(help_text="Total length of the track in inches")
    timber_spacing = models.FloatField(help_text="Spacing between timbers in inches")
    chair_alignment = models.CharField(
        max_length=20,
        choices=CHAIR_ALIGNMENT_CHOICES,
        help_text="Chair alignment pattern",
    )
    is_straight = models.BooleanField(default=True, help_text="Is the track straight?")
    kerf_adjustment = models.FloatField(
        blank=True, null=True, help_text="Adjustment for material kerf or tolerances"
    )
    flange_width = models.FloatField(
        blank=True, null=True, help_text="Width of the flange in inches"
    )
    flange_depth = models.FloatField(
        blank=True, null=True, help_text="Depth of the flange in inches"
    )
    chair_type = models.ForeignKey(
        BullheadChairs, on_delete=models.CASCADE, related_name="tracks"
    )

    def __str__(self):
        return f"Track {self.id}"


# Timber Table
class Timber(models.Model):
    track = models.ForeignKey(
        Track, on_delete=models.CASCADE, related_name="timbers"
    )
    length = models.FloatField()
    width = models.FloatField()
    depth = models.FloatField()
    position = models.FloatField()
    chair = models.ForeignKey(
        BullheadChairs, on_delete=models.CASCADE, related_name="timbers"
    )

    def __str__(self):
        return f"Timber {self.id} for Track {self.track.id}"


# User Profile Table
class UserProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile"
    )
    role = models.CharField(
        max_length=20,
        choices=[
            ("superuser", "Superuser"),
            ("admin", "Admin"),
            ("user", "User"),
        ],
        default="user",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.role.capitalize()}"


# STL Download Log Table
class STLDownloadLog(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="downloads"
    )
    chair = models.ForeignKey(
        BullheadChairs,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="downloads",
    )
    track = models.ForeignKey(
        Track,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="downloads",
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    file_path = models.CharField(
        max_length=255, help_text="Path to the downloaded STL file"
    )

    def __str__(self):
        return f"{self.user.username} downloaded {self.file_path} on {self.timestamp}"
