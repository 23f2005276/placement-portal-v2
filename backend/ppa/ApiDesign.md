# Important

- put, patch, post (use carefully according to semantics) , put for complete replacement, patch for partial modification, post for creating something new

# Auth Apis

- cache branches and industries in the get requests
- signup ke baad the user should be automatically be redirected to the appropriate dashboard according to the role
- login ke baad the user should be automatically be redirected to the appropriate dashboard, if already loggedin (localStorage has jwt then just redirect the user to the dashboard, same goes for signup if the user logged in then redirect to the actual page)

# Admin Apis

### dashboard api

- 1 call for giving the numbers of total students, companies and total placement drives (cache this)
- 1 call for getting all the companies, students from their tables, while also taking students and joining them with the PPAusers table for the full name (cache this) 
    - isi ka ek post version me we update the status of the company hrs and students as active or blacklisted
- 1 call for getting all the pending approvals of companies and placement drives
    - isi ka ek post version me we update the status of the companies and drives as approved

### profile api 
- get api to get the admin details 
- post api to update the name and contact number of the admin

### placements drives api
- get api with path parameter (status of the placement drive), all ke liye all placement drives, usi hisaab se har category wise placement drives served (cache this)
- patch api for updating the status of the placement drive (approved, or rejected, default would be pending)

### reports api
- get selected students count from the studentapplications table
- using the StudentPlacementStatus table to fetch the student placement percentage in the reports api, when the student applies to even on a single placement drive, then uska status becomes applied and percentage will be calculated ki out of all the applied how many of them have been selected (cache this)
- placement drives me se use package data to calculate the average package of the placed students only
- ek chart banane wala api rahega ki har ek particular branch se kitne percentage logo ka placement ho gaya hai karke, and serve the data in proper format which the client can use to render charts and stuff
- last wala table we can calculate using the CompanyPlacementData table, where calculation of the new average package can be easily done using the old average package value

# Company apis

### dashboard apis
- company details from the company table, placement drive details, students applied of the drive details can be extracted from the students_applied relation in placement_drive table
- 