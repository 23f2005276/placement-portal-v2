# Placement Portal Features & Constraints

This document catalogs all system features and architectural constraints for reference across the application's components.

## Auth & Session Flow
* **Syncing Local Storage**: Upon successful login or registration, the `user_id` returned by the backend is stored in `localStorage` under key `user_id`. Redirection or logout deletes this key.
* **Redirection Safety**: Routing verification matches subpaths (e.g. `/company_hr`) to prevent clearing valid deep routes on component reload.

## Role-Based Access Control (RBAC)
* **JWT Enforced Checks**: The backend enforces role restrictions via `@check_jwt_and_role("<role_name>")`.
* **Argument Inspection Rules**:
  - `GET` requests check the `user_id` query string parameter.
  - `POST`, `PATCH`, and `PUT` requests check the `user_id` inside the JSON body payload.
  - The parameter value must match the token's authenticated subject (`sub`) ID.

## Admin Role
* **Approvals & Entity Status**:
  - Approves or blacklists users (companies and students) and placement drives.
  - Pending entities are restricted from dashboard activities.
* **Placement Drives Control**:
  - Lists all placement drives in a table. Does not show Drive ID.
  - Top filtering by approved drives, closed drives, pending drives, and rejected drives. No search bar.
  - Action buttons: Eye icon to view drive details (read-only); Check and Cross icons to Approve or Reject (active for pending drives only).
* **Placement Reports**:
  - Displays summary statistics: Total Students Placed, Overall Placement Rate (percentage of placed students relative to total student users), Average Package (LPA), and Highest Package (LPA).
  - Renders Top Recruiting Companies list (Company Name, Sector, Students Hired count, and Average Package).
  - No charts are displayed.


## Company HR Role
* **Create Placement Drive**:
  - Requires admin approval before becoming active.
  - Selection of eligible branches uses a multi-select checkbox grid.
* **Company Dashboard**:
  - Left card: Initials-based avatar, company name, industry, and total active drives. No Account Status is visible.
  - Right card: Table of approved active drives only.
* **Placement Drives Page**:
  - Lists all drives created by the company (Approved, Pending, Closed, Rejected). No Drive ID is shown.
  - Allows closing active drives using the Stop Icon. Disallowed for non-approved drives on client and server.
* **Drive Applications Page**:
  - Access is restricted on client and server to approved and closed drives. Disallowed for pending/rejected drives.
  - Shows candidate applications with CGPA, branch, and status.
  - Allows HR to Shortlist, Select, or Reject candidate applications.
  - **Status Change Hook**: When a student application status is updated to `"selected"`, the student's status is set as `"placed"` in `StudentPlacementStatus`.
* **HR Profile Page**:
  - Omits Account Status line. Editable HR contact details and read-only company details.

## Student Role
* **Eligible Drives Filter**:
  - Server filters drives based on the student's branch ID. Only approved drives are returned.
  - Applications are disallowed if the drive is pending, closed, rejected, or if the deadline has passed.
  - Students cannot apply to the same drive multiple times.
* **Student Dashboard**:
  - Left card: Shows student name, branch, CGPA, and resume file link. No telephone.
  - Right card:
    - Upper table: Lists eligible placement drives. Clicking view details opens the drive details page.
    - Bottom table: Lists status of submitted applications.
* **Student Profile Page**:
  - Details modeled on registration. Branch and CGPA are read-only on both client and server.
  - Skills section: Add or remove keyword tags, saved in `student_skills` and `skills` tables.
  - Resume Management: View current resume, upload new PDF. Resumes stored in `files/` folder as `resume_student_<id>.pdf`, with URL updated in DB.
* **Placement Reports Page**:
  - Shows statistics (total drives applied, shortlisted, placed, and rejected count).
