# Project Rules

- **No Code Comments**: Do not write comments (single-line, multi-line, docstrings, or template comments) in any newly written or modified source code files, as it flags the code as AI-generated.
- **HTTP Parameter Guidelines**:
  - GET requests must accept `user_id` as a query parameter (e.g. `?user_id=123`).
  - POST, PATCH, and PUT requests must accept `user_id` inside the JSON body as the key `"user_id"`.

