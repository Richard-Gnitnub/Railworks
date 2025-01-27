Here’s the updated **API Design Document** with **Django Ninja** incorporated into the existing architecture:

---

# **API Design Document for Hybrid REST and Async API**

## **Introduction**
This document outlines the design for a hybrid API combining **Django Ninja**, Django REST Framework (DRF), and Django Async capabilities. The API is designed to handle CRUD operations, asynchronous tasks like STL file generation, and support multiple concurrent users efficiently.

---

## **Goals**
1. Provide robust CRUD operations for managing track components (e.g., tracks, timbers, chairs).
2. Support high-performance asynchronous endpoints for computationally intensive tasks like STL generation.
3. Ensure scalability to accommodate multiple concurrent users.
4. Maintain simplicity and compatibility for developers and users.
5. Allow for seamless integration with third-party tools and monitoring systems.

---

## **Core Features**

### **1. User Management**
- **Endpoints**:
  - `POST /api/register/`: Register new users.
  - `POST /api/login/`: Authenticate users and return tokens (JWT).
  - `GET /api/profile/`: Retrieve user profile information.
  - `PUT /api/profile/`: Update user information.

- **Key Points**:
  - Use Django's built-in `User` model with custom extensions.
  - JWT-based authentication for secure and stateless interactions.

---

### **2. Track and Component Management**
- **Endpoints** (Implemented with **Django Ninja**):
  - `GET /api/tracks/`: List all tracks.
  - `POST /api/tracks/`: Create new track configurations.
  - `GET /api/tracks/{id}/`: Retrieve details of a specific track.
  - `PUT /api/tracks/{id}/`: Update an existing track.
  - `DELETE /api/tracks/{id}/`: Delete a track.

- **Key Points**:
  - CRUD operations are now implemented using Django Ninja's type-safe schema-based endpoints.
  - Support for filtering, pagination, and schema validation.

---

### **3. STL Generation**
- **Endpoints**:
  - `POST /api/stl/generate/`: Initiate STL generation with track parameters.
  - `GET /api/stl/status/{task_id}/`: Check the status of the generation task.
  - `GET /api/stl/download/{file_id}/`: Download the generated STL file.

- **Key Points**:
  - Use Django Ninja for clean schema validation and asynchronous support.
  - Offload intensive tasks to Celery workers.
  - Provide secure and time-limited download links for STL files.

---

### **4. STL Download Logging**
- **Endpoints**:
  - `GET /api/downloads/`: List user-specific download history.
  - `DELETE /api/downloads/{id}/`: Delete a specific log entry.

- **Key Points**:
  - Use Django Ninja's schema capabilities for validating and returning detailed log records.
  - Maintain an audit trail for downloads and user activity.

---

## **Architecture Overview**

### **Django Ninja Integration**
- **Django Ninja**: A modern schema-based framework for defining type-safe REST APIs.
  - Combines well with Django Async views and Celery tasks.
  - Reduces boilerplate while improving maintainability and documentation.

### **Hybrid Approach**
- **Django Ninja**: Handles all CRUD operations, validation, and schema generation.
- **Django Async Views**: Implemented for endpoints requiring high concurrency (e.g., STL generation).
- **Celery with Redis**: Manages long-running or computationally intensive tasks like STL generation.

---

## **Request-Response Flow**

### **Example: STL Generation Workflow**
1. **Initiate Task**:
   - Client sends a `POST` request to `/api/stl/generate/` with track parameters.
   - Django Ninja validates inputs and queues the task using Celery.
   - Response includes a `task_id` for tracking.

2. **Check Status**:
   - Client sends a `GET` request to `/api/stl/status/{task_id}/`.
   - The API checks the task status in Redis and responds with `pending`, `in-progress`, or `completed`.

3. **Download File**:
   - Upon task completion, a secure file URL is generated.
   - Client downloads the file using `/api/stl/download/{file_id}/`.

---

## **Authentication**
- **JWT Authentication**:
  - Used for all endpoints to ensure secure and stateless communication.
  - Tokens expire after a set period and require renewal.

---

## **Error Handling**
1. **Validation Errors**:
   - Return HTTP 422 with detailed error messages if schema validation fails.
2. **Authentication Errors**:
   - Return HTTP 401 for invalid or missing tokens.
3. **Task Errors**:
   - Return HTTP 500 with a descriptive message if STL generation fails.
4. **Rate Limiting**:
   - Implement rate limits to prevent abuse of high-load endpoints.

---

## **Monitoring and Logging**
- **Monitoring Tools**:
  - Use Prometheus and Grafana for tracking API performance.
  - Celery Flower for monitoring task status.

- **Logging**:
  - Maintain detailed logs for API requests and task statuses.
  - Log errors with sufficient context for debugging.

---

## **Future Enhancements**
1. **GraphQL Integration**:
   - Add support for GraphQL to provide flexible querying for complex data relationships.
2. **Advanced STL Configurations**:
   - Extend STL generation to handle advanced configurations like turnouts and curves.
3. **Role-Based Access Control (RBAC)**:
   - Implement RBAC for different user tiers (e.g., admin, premium users).
4. **Real-Time Updates**:
   - Introduce WebSocket-based real-time updates for task statuses.

---

## **Conclusion**
This updated API design leverages **Django Ninja** for type-safe and schema-driven REST endpoints, combined with Celery and Django Async for efficient task management. The architecture balances simplicity and scalability, ensuring the system can accommodate both developers' and users' needs.

---
