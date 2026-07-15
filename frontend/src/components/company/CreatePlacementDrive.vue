<script setup>
import { onMounted, ref, computed } from "vue";
import { useRouter } from "vue-router";

const apiUrl = import.meta.env.VITE_API_BASE_URL;
const router = useRouter();

const branchesList = ref([]);
const jobTitle = ref("");
const location = ref("");
const salaryPackage = ref("");
const applicationDeadline = ref("");
const jobDescription = ref("");
const eligibleBranches = ref([]);
const minCgpa = ref("");
const eligibleYear = ref("");

const errorMsg = ref("");
const successMsg = ref("");

const isAllSelected = computed(() => {
  return branchesList.value.length > 0 && eligibleBranches.value.length === branchesList.value.length;
});

const toggleSelectAll = (event) => {
  if (event.target.checked) {
    eligibleBranches.value = [...branchesList.value];
  } else {
    eligibleBranches.value = [];
  }
};

const fetchBranches = async () => {
  const response = await fetch(`${apiUrl}/api/signup?category=student`);
  if (response.ok) {
    const data = await response.json();
    branchesList.value = data.branches_list.content;
  }
};

const handleCancel = () => {
  router.push("/company_hr");
};

const handleCreate = async () => {
  const userId = localStorage.getItem("user_id");
  if (!userId) {
    errorMsg.value = "Session user ID not found. Please log in.";
    return;
  }

  if (
    !jobTitle.value.trim() ||
    !salaryPackage.value ||
    !applicationDeadline.value ||
    !jobDescription.value.trim() ||
    eligibleBranches.value.length === 0 ||
    !minCgpa.value ||
    !eligibleYear.value
  ) {
    errorMsg.value = "Please fill in all required fields.";
    return;
  }

  const formattedDeadline = `${applicationDeadline.value}T23:59:00`;

  const payload = {
    user_id: parseInt(userId),
    job_title: jobTitle.value.trim(),
    job_description: jobDescription.value.trim(),
    min_cgpa: parseFloat(minCgpa.value),
    eligible_year: parseInt(eligibleYear.value),
    location: location.value.trim() || "Remote",
    salary_package: parseInt(salaryPackage.value),
    application_deadline: formattedDeadline,
    eligible_branches: Array.from(eligibleBranches.value)
  };

  const response = await fetch(`${apiUrl}/api/company_hr/create`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    credentials: "include",
    body: JSON.stringify(payload)
  });

  if (response.ok) {
    successMsg.value = "Placement drive created successfully!";
    errorMsg.value = "";
    
    jobTitle.value = "";
    location.value = "";
    salaryPackage.value = "";
    applicationDeadline.value = "";
    jobDescription.value = "";
    eligibleBranches.value = [];
    minCgpa.value = "";
    eligibleYear.value = "";
  } else {
    const errorData = await response.json();
    errorMsg.value = errorData.message || "Failed to create placement drive.";
    successMsg.value = "";
  }
};

onMounted(async () => {
  await fetchBranches();
});
</script>

<template>
  <div class="container-fluid py-4 font-segoe">
    <div class="row mb-2">
      <div class="col-12">
        <h2 class="fw-bold text-dark mb-1">Create New Placement Drive</h2>
        <p class="text-secondary m-0">Configure details and eligibility criteria for your upcoming hiring event.</p>
      </div>
    </div>

    <div v-if="errorMsg" class="alert alert-danger my-3" role="alert">
      {{ errorMsg }}
    </div>
    <div v-if="successMsg" class="alert alert-success my-3" role="alert">
      {{ successMsg }}
    </div>

    <div class="card border border-secondary-subtle rounded-3 shadow-sm bg-white p-4 mb-4 mt-3" style="max-width: 1200px;">
      <div class="d-flex align-items-center gap-2 mb-4 pb-2 border-bottom">
        <div class="text-primary">
          <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" fill="currentColor" class="bi bi-briefcase" viewBox="0 0 16 16">
            <path d="M6.5 1A1.5 1.5 0 0 0 5 2.5V3H1.5A1.5 1.5 0 0 0 0 4.5v8A1.5 1.5 0 0 0 1.5 14h13a1.5 1.5 0 0 0 1.5-1.5v-8A1.5 1.5 0 0 0 14.5 3H11v-.5A1.5 1.5 0 0 0 9.5 1h-3zm0 1h3a.5.5 0 0 1 .5.5V3H6v-.5a.5.5 0 0 1 .5-.5zm1.886 6.914L15 7.151V12.5a.5.5 0 0 1-.5.5h-13a.5.5 0 0 1-.5-.5V7.15l6.614 1.764a1.5 1.5 0 0 0 .772 0zM1.5 4h13a.5.5 0 0 1 .5.5v1.616L8.129 7.948a.5.5 0 0 1-.258 0L1 6.116V4.5a.5.5 0 0 1 .5-.5z"/>
          </svg>
        </div>
        <h5 class="fw-bold text-dark m-0">Job Details</h5>
      </div>

      <div class="row g-3">
        <div class="col-12">
          <label class="form-label fw-semibold text-secondary" style="font-size: 0.8rem;">Job Title *</label>
          <input v-model="jobTitle" type="text" class="form-control border border-secondary-subtle" placeholder="e.g. Software Development Engineer (SDE I)" />
        </div>

        <div class="col-12">
          <label class="form-label fw-semibold text-secondary" style="font-size: 0.8rem;">Location</label>
          <div class="input-group">
            <span class="input-group-text bg-light text-secondary border border-secondary-subtle border-end-0">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-geo-alt" viewBox="0 0 16 16">
                <path d="M12.166 8.94c-.524 1.062-1.234 2.12-1.96 3.07A31.493 31.493 0 0 1 8 14.58a31.481 31.481 0 0 1-2.206-2.57c-.726-.95-1.436-2.008-1.96-3.07C3.304 7.867 3 6.862 3 6a5 5 0 0 1 10 0c0 .862-.305 1.867-.834 2.94zM8 16s6-5.686 6-10A6 6 0 0 0 2 6c0 4.314 6 10 6 10z"/>
                <path d="M8 8a2 2 0 1 1 0-4 2 2 0 0 1 0 4zm0 1a3 3 0 1 0 0-6 3 3 0 0 0 0 6z"/>
              </svg>
            </span>
            <input v-model="location" type="text" class="form-control border border-secondary-subtle border-start-0 ps-0" placeholder="e.g. Bangalore, Remote, Pan India" />
          </div>
        </div>

        <div class="col-12 col-md-6">
          <label class="form-label fw-semibold text-secondary" style="font-size: 0.8rem;">Salary / Package (CTC) *</label>
          <div class="input-group">
            <span class="input-group-text bg-light text-secondary border border-secondary-subtle border-end-0">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-cash-stack" viewBox="0 0 16 16">
                <path d="M1 3a1 1 0 0 1 1-1h12a1 1 0 0 1 1 1H1zm7 8a2 2 0 1 0 0-4 2 2 0 0 0 0 4z"/>
                <path d="M0 5a1 1 0 0 1 1-1h14a1 1 0 0 1 1 1v8a1 1 0 0 1-1 1H1a1 1 0 0 1-1-1V5zm3 0a2 2 0 0 1-2 2v4a2 2 0 0 1 2 2h10a2 2 0 0 1 2-2V7a2 2 0 0 1-2-2H3z"/>
              </svg>
            </span>
            <input v-model="salaryPackage" type="number" class="form-control border border-secondary-subtle border-start-0 ps-0" placeholder="e.g. 12" />
          </div>
          <div class="form-text text-secondary mt-1" style="font-size: 0.75rem;">Enter CTC as a integer value (e.g. 12 for 12 LPA).</div>
        </div>

        <div class="col-12 col-md-6">
          <label class="form-label fw-semibold text-secondary" style="font-size: 0.8rem;">Application Deadline *</label>
          <div class="input-group">
            <span class="input-group-text bg-light text-secondary border border-secondary-subtle border-end-0">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-calendar-event" viewBox="0 0 16 16">
                <path d="M11 6.5a.5.5 0 0 1 .5-.5h1a.5.5 0 0 1 .5.5v1a.5.5 0 0 1-.5.5h-1a.5.5 0 0 1-.5-.5v-1z"/>
                <path d="M3.5 0a.5.5 0 0 1 .5.5V1h8V.5a.5.5 0 0 1 1 0V1h1a2 2 0 0 1 2 2v11a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V3a2 2 0 0 1 2-2h1V.5a.5.5 0 0 1 .5-.5zM1 4v10a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V4H1z"/>
              </svg>
            </span>
            <input v-model="applicationDeadline" type="date" class="form-control border border-secondary-subtle border-start-0 ps-0" />
          </div>
        </div>

        <div class="col-12">
          <label class="form-label fw-semibold text-secondary" style="font-size: 0.8rem;">Job Description *</label>
          <textarea v-model="jobDescription" class="form-control border border-secondary-subtle" rows="5" placeholder="Detail the role responsibilities, requirements, and benefits..."></textarea>
        </div>
      </div>
    </div>

    <div class="card border border-secondary-subtle rounded-3 shadow-sm bg-white p-4 mb-4" style="max-width: 1200px;">
      <div class="d-flex align-items-center gap-2 mb-4 pb-2 border-bottom">
        <div class="text-primary">
          <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" fill="currentColor" class="bi bi-mortarboard" viewBox="0 0 16 16">
            <path d="M8.211 2.047a.5.5 0 0 0-.422 0l-7.135 3.7A.5.5 0 0 0 0 6.201v2.165c0 .325.264.589.589.589H1.41c.325 0 .589-.264.589-.589V6.76l5.779 3.003a.5.5 0 0 0 .444 0L14 6.76v5.184a.5.5 0 0 0 .324.468l2 1a.5.5 0 0 0 .676-.468v-6.75a.5.5 0 0 0-.21-.402l-7.5-3.75zm-6.735 4.6L8 3.252l6.524 3.395-6.524 3.395L1.476 6.647z"/>
            <path d="M4.176 9.032a.5.5 0 0 0-.656.327 5.5 5.5 0 0 0-.004 2.842.5.5 0 0 0 .66.32c1.785-.595 3.342-1.39 4.324-1.956.126-.073.125-.27-.004-.34-1.127-.615-2.614-1.332-4.32-1.193z"/>
          </svg>
        </div>
        <h5 class="fw-bold text-dark m-0">Eligibility Criteria</h5>
      </div>

      <div class="row g-3">
        <div class="col-12">
          <label class="form-label fw-semibold text-secondary mb-2" style="font-size: 0.8rem;">Eligible Branches *</label>
          <div class="row g-2 border border-secondary-subtle rounded-3 p-3 bg-light">
            <div class="col-12 col-sm-6 col-md-4" v-for="branch in branchesList" :key="branch">
              <div class="form-check">
                <input 
                  type="checkbox" 
                  :id="'branch-' + branch" 
                  :value="branch" 
                  v-model="eligibleBranches" 
                  class="form-check-input border-secondary-subtle" 
                />
                <label :for="'branch-' + branch" class="form-check-label text-dark fw-semibold" style="font-size: 0.85rem; cursor: pointer;">
                  {{ branch }}
                </label>
              </div>
            </div>
            <div class="col-12 mt-2 pt-2 border-top">
              <div class="form-check">
                <input 
                  type="checkbox" 
                  id="select-all-branches" 
                  :checked="isAllSelected" 
                  @change="toggleSelectAll" 
                  class="form-check-input border-secondary-subtle" 
                />
                <label for="select-all-branches" class="form-check-label text-primary fw-semibold" style="font-size: 0.85rem; cursor: pointer;">
                  Select All
                </label>
              </div>
            </div>
          </div>
        </div>

        <div class="col-12 col-md-6">
          <label class="form-label fw-semibold text-secondary" style="font-size: 0.8rem;">Minimum CGPA *</label>
          <input v-model="minCgpa" type="number" step="any" class="form-control border border-secondary-subtle" placeholder="e.g. 7.5" />
        </div>

        <div class="col-12 col-md-6">
          <label class="form-label fw-semibold text-secondary" style="font-size: 0.8rem;">Eligible Year of Study *</label>
          <select v-model="eligibleYear" class="form-select border border-secondary-subtle">
            <option disabled value="">Select Year</option>
            <option value="1">First Year (1)</option>
            <option value="2">Second Year (2)</option>
            <option value="3">Third Year (3)</option>
            <option value="4">Fourth Year (4)</option>
          </select>
        </div>
      </div>
    </div>

    <div class="row" style="max-width: 1200px;">
      <div class="col-12 d-flex justify-content-end gap-2">
        <button @click="handleCancel" class="btn btn-outline-secondary px-4 py-2 fw-semibold">Cancel</button>
        <button @click="handleCreate" class="btn btn-primary px-4 py-2 fw-semibold d-flex align-items-center gap-2">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-plus-circle" viewBox="0 0 16 16">
            <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z"/>
            <path d="M8 4a.5.5 0 0 1 .5.5v3h3a.5.5 0 0 1 0 1h-3v3a.5.5 0 0 1-1 0v-3h-3a.5.5 0 0 1 0-1h3v-3A.5.5 0 0 1 8 4z"/>
          </svg>
          Create Drive
        </button>
      </div>
    </div>
  </div>
</template>
