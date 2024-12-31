# Database Design Documentation for Lightweight Track Builder

## Overview
The Lightweight Track Builder is a Django-based application designed for creating model railway track components adhering to REA Bullhead standards. The database schema ensures that all track configurations, components, and user actions are structured for flexibility, scalability, and ease of management.

---

## Models

### **1. Gauge**
Represents different track gauge widths.
- **Fields:**
  - `name`: Unique name for the gauge (e.g., "Standard Gauge").
  - `width`: Gauge width in millimetres.
  - `description`: Optional textual description.

---

### **2. Bullhead Chairs**
Defines characteristics of bullhead rail chairs.
- **Fields:**
  - `type`: Type of chair (Standard 1, Large 1, Special Chair).
  - `plinth_thickness`: Thickness of the plinth in inches.
  - `edge_thickness`: Thickness of the edge in inches.
  - `seat_thickness`: Thickness of the seat under the rail in inches.
  - `key_length`: Length of the rail keys in inches.
  - `key_deformation`: Deformation factor for key fitting.
  - `key_pad_taper`: Taper of the key pad.
  - `boss_height`: Height of the boss in inches.
  - `ferrule_height`: Height of the ferrule in inches.
  - `bolt_head_height`: Height of the bolt head in inches.
  - `boss_diameter`: Diameter of the boss in inches.
  - `hole_diameter`: Diameter of the ferrule or hole in inches.

---

### **3. Bullhead Jaw Section**
Defines jaw sections attached to bullhead chairs.
- **Fields:**
  - `chair`: Foreign key to `BullheadChairs`.
  - `jaw_type`: Type of jaw (Outer, Inner).
  - `section`: Section type (Top, Middle, Seat, Plinth).
  - `rib_depth`: Depth of the rib in inches.
  - `rib_width`: Width of the rib in inches.
  - `rib_space`: Spacing between ribs in inches.
  - `rib_count`: Number of ribs.
  - `half_width`: Half-width of the jaw section in inches.
  - `depth`: Depth of the jaw section in inches.
  - `fillet_radius`: Radius of the fillet in inches.
  - `slope`: Slope of the section in degrees.
  - `bolt_position`: Position of the bolt in inches (optional).

---

### **4. Bullhead Key**
Defines key characteristics for bullhead rail chairs.
- **Fields:**
  - `chair`: Foreign key to `BullheadChairs`.
  - `type`: Type of key (Solid, Loose).
  - `length`: Length of the key in inches.
  - `pad_length`: Length of the key pad in inches.
  - `deformation`: Deformation factor for the key.

---

### **5. Bullhead Boss and Ferrule**
Defines boss and ferrule components for bullhead chairs.
- **Fields:**
  - `chair`: Foreign key to `BullheadChairs`.
  - `component`: Type of component (Boss, Ferrule, Bolt).
  - `height`: Height of the component in inches.
  - `diameter`: Diameter of the component in inches (optional).

---

### **6. Track**
Defines characteristics of railway tracks.
- **Fields:**
  - `gauge`: Foreign key to `Gauge`.
  - `total_length`: Total length of the track in inches.
  - `timber_spacing`: Spacing between timbers in inches.
  - `chair_alignment`: Alignment pattern of chairs (Opposite, Staggered).
  - `is_straight`: Boolean field indicating if the track is straight.
  - `kerf_adjustment`: Adjustment for material kerf or tolerances.
  - `flange_width`: Width of the flange in inches.
  - `flange_depth`: Depth of the flange in inches.
  - `chair_type`: Foreign key to `BullheadChairs`.

---

### **7. Timber**
Defines timber characteristics for tracks.
- **Fields:**
  - `track`: Foreign key to `Track`.
  - `length`: Length of the timber in inches.
  - `width`: Width of the timber in inches.
  - `depth`: Depth of the timber in inches.
  - `position`: Position of the timber along the track.
  - `chair`: Foreign key to `BullheadChairs`.

---

### **8. User Profile**
Manages user roles and metadata.
- **Fields:**
  - `user`: One-to-one relationship with Django's `User` model.
  - `role`: Role of the user (Superuser, Admin, User).
  - `created_at`: Timestamp of profile creation.

---

### **9. STL Download Log**
Tracks STL file downloads by users.
- **Fields:**
  - `user`: Foreign key to `User`.
  - `chair`: Foreign key to `BullheadChairs` (optional).
  - `track`: Foreign key to `Track` (optional).
  - `timestamp`: Timestamp of the download.
  - `file_path`: Path to the downloaded STL file.

---

## Relationships and Constraints
- **Gauge**:
  - One-to-Many with `Track`.
- **BullheadChairs**:
  - One-to-Many with `BullheadJawSection`.
  - One-to-Many with `BullheadKey`.
  - One-to-Many with `BullheadBossAndFerrule`.
  - One-to-Many with `Track`.
  - One-to-Many with `Timber`.
- **Track**:
  - One-to-Many with `Timber`.
  - One-to-Many with `STLDownloadLog`.
- **User Profile**:
  - One-to-One with Django's `User`.
- **STLDownloadLog**:
  - Tracks actions for auditing and user accountability.

---

## Design Highlights
- **Normalisation:**
  - The database adheres to third normal form (3NF) to reduce redundancy and ensure data consistency.
- **Validation:**
  - Custom validation logic (e.g., plinth thickness cannot exceed 10 inches).
- **Scalability:**
  - Modular design allows easy addition of new chair or track types.
- **User Tracking:**
  - STL downloads are logged for accountability and usage analytics.
- **API Considerations:**
  - The database schema is optimised for API performance, ensuring fast query response times and minimal payloads.
  - Clear relationships between models facilitate efficient API endpoints, supporting both detailed and aggregated data retrieval.

---

## Future Enhancements
- Add tables for curved tracks and turnouts.
- Introduce user activity logs for comprehensive auditing.
- Integrate mesh inspection results into the database schema.
- Optimise for PostgreSQL for production-grade deployments.

