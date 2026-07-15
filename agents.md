# Agent Rules and Internalized Constraints

This file documents the project rules, constraints, and instructions internalized by coding agents from workspace configurations and guidelines.

---

## 1. Code Construction Constraints

* **No Code Comments**: 
  - Do **not** write comments (single-line comments, multi-line blocks, docstrings, or template comments) in any newly written or modified source code files (Python, Vue, JavaScript).
  - Commented code flags files as AI-generated and must be avoided.

---

## 2. API Parameter Conventions

* **HTTP Parameter Rules**:
  - **GET Requests**: Must expect the `user_id` parameter inside the query string format (e.g. `/api/...?user_id=123`).
  - **POST/PATCH/PUT Requests**: Must expect the `user_id` parameter inside the JSON request body (e.g., `{"user_id": 123}`).
  - These values are checked by the RBAC middleware against the JWT token identity.

---

## 3. Technology Stack & Design Guidelines

* **Frontend**:
  - Built with Vue 3 (Composition API using `<script setup>`), Vite, and Bootstrap 5.
  - Styling utilizes Vanilla CSS where custom layout is needed. Standard Bootstrap classes should be leveraged cleanly.
  - Always design with rich aesthetics (clean card structures, proper contrast, rounded borders, clear status badges, and hover animations).

* **Backend**:
  - Built with Flask, Flask-RESTful, and Flask-SQLAlchemy (SQLAlchemy 2.0 styled declarative mapping).
  - Database runs on SQLite (`ppa.db`).

---

## 4. Key Rules and Security Logic

* **Access Restrictions**:
  - Companies cannot see applications of a drive if the drive is in `pending` or `rejected` status.
  - Recruiter companies can only close drives that are in `approved` status. Non-approved drives cannot be closed from either the client or server.
  - Admin approval/rejection triggers only work for drives with a `pending` status.
