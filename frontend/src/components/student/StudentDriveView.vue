<script setup>
import { onMounted, ref } from "vue";
import { useRoute, useRouter } from "vue-router";

const apiUrl = import.meta.env.VITE_API_BASE_URL;
const route = useRoute();
const router = useRouter();

const driveId = ref(null);
const drive = ref(null);
const loading = ref(true);
const errorMsg = ref("");
const successMsg = ref("");

const fetchDriveDetails = async () => {
  const userId = localStorage.getItem("user_id");
  if (!userId) {
    errorMsg.value = "Session user ID not found. Please log in.";
    loading.value = false;
    return;
  }

  const response = await fetch(`${apiUrl}/api/student/drive?user_id=${userId}&drive_id=${driveId.value}`, {
    method: "GET",
    credentials: "include"
  });

  if (response.ok) {
    drive.value = await response.json();
  } else {
    const errorData = await response.json();
    errorMsg.value = errorData.message || "Failed to load drive details.";
  }
  loading.value = false;
};

const handleApply = async () => {
  const userId = localStorage.getItem("user_id");
  if (!userId) return;

  const response = await fetch(`${apiUrl}/api/student/apply`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    credentials: "include",
    body: JSON.stringify({
      user_id: parseInt(userId),
      drive_id: parseInt(driveId.value)
    })
  });

  if (response.ok) {
    successMsg.value = "You have successfully applied to this placement drive!";
    if (drive.value) {
      drive.value.applied = true;
    }
  } else {
    const errorData = await response.json();
    errorMsg.value = errorData.message || "Failed to submit application.";
  }
};

const handleBack = () => {
  router.push("/student");
};

const formatDate = (isoString) => {
  if (!isoString) return "";
  const date = new Date(isoString);
  return date.toLocaleString();
};

onMounted(async () => {
  driveId.value = route.query.id;
  await fetchDriveDetails();
});
</script>

<template>
  <div class="container-fluid py-4 font-segoe">
    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>

    <div v-else-if="errorMsg && !drive" class="alert alert-danger" role="alert">
      {{ errorMsg }}
      <div class="mt-3">
        <button @click="handleBack" class="btn btn-secondary btn-sm">Back to Dashboard</button>
      </div>
    </div>

    <div v-else class="mx-auto" style="max-width: 1000px;">
      <div class="row align-items-center mb-4 g-3">
        <div class="col-12 col-md-8">
          <nav aria-label="breadcrumb" style="font-size: 0.85rem;">
            <ol class="breadcrumb mb-2">
              <li class="breadcrumb-item"><span class="text-secondary" style="cursor: pointer;" @click="handleBack">Dashboard</span></li>
              <li class="breadcrumb-item active text-dark fw-semibold" aria-current="page">Drive Details</li>
            </ol>
          </nav>
          <h2 class="fw-bold text-dark mb-1">{{ drive.company_name }} - {{ drive.job_title }}</h2>
          <p class="text-secondary m-0">Review job description, package levels, and branches before applying.</p>
        </div>
        <div class="col-12 col-md-4 d-flex justify-content-md-end gap-2">
          <button @click="handleBack" class="btn btn-outline-secondary px-4 fw-semibold">
            Back
          </button>
          <button 
            v-if="!drive.applied" 
            @click="handleApply" 
            class="btn btn-primary px-4 fw-semibold"
          >
            Apply to Drive
          </button>
          <button 
            v-else 
            disabled 
            class="btn btn-success px-4 fw-semibold disabled"
          >
            Already Applied
          </button>
        </div>
      </div>

      <div v-if="errorMsg" class="alert alert-danger my-3" role="alert">
        {{ errorMsg }}
      </div>
      <div v-if="successMsg" class="alert alert-success my-3" role="alert">
        {{ successMsg }}
      </div>

      <div class="card border border-secondary-subtle rounded-3 shadow-sm bg-white p-4 mb-4">
        <div class="d-flex align-items-center gap-2 mb-4 pb-2 border-bottom">
          <div class="text-primary">
            <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" fill="currentColor" class="bi bi-briefcase" viewBox="0 0 16 16">
              <path d="M6.5 1A1.5 1.5 0 0 0 5 2.5V3H1.5A1.5 1.5 0 0 0 0 4.5v8A1.5 1.5 0 0 0 1.5 14h13a1.5 1.5 0 0 0 1.5-1.5v-8A1.5 1.5 0 0 0 14.5 3H11v-.5A1.5 1.5 0 0 0 9.5 1h-3zm0 1h3a.5.5 0 0 1 .5.5V3H6v-.5a.5.5 0 0 1 .5-.5zm1.886 6.914L15 7.151V12.5a.5.5 0 0 1-.5.5h-13a.5.5 0 0 1-.5-.5V7.15l6.614 1.764a1.5 1.5 0 0 0 .772 0zM1.5 4h13a.5.5 0 0 1 .5.5v1.616L8.129 7.948a.5.5 0 0 1-.258 0L1 6.116V4.5a.5.5 0 0 1 .5-.5z"/>
            </svg>
          </div>
          <h5 class="fw-bold text-dark m-0">Job Details</h5>
        </div>

        <div class="row g-3">
          <div class="col-12 col-md-6">
            <label class="form-label fw-semibold text-secondary" style="font-size: 0.8rem;">Job Title</label>
            <input :value="drive.job_title" disabled type="text" class="form-control border border-secondary-subtle bg-light text-dark fw-semibold" />
          </div>

          <div class="col-12 col-md-6">
            <label class="form-label fw-semibold text-secondary" style="font-size: 0.8rem;">Location</label>
            <input :value="drive.location" disabled type="text" class="form-control border border-secondary-subtle bg-light text-dark fw-semibold" />
          </div>

          <div class="col-12 col-md-6">
            <label class="form-label fw-semibold text-secondary" style="font-size: 0.8rem;">Salary / Package (CTC)</label>
            <input :value="drive.salary_package + ' LPA'" disabled type="text" class="form-control border border-secondary-subtle bg-light text-dark fw-semibold" />
          </div>

          <div class="col-12 col-md-6">
            <label class="form-label fw-semibold text-secondary" style="font-size: 0.8rem;">Application Deadline</label>
            <input :value="formatDate(drive.application_deadline)" disabled type="text" class="form-control border border-secondary-subtle bg-light text-dark fw-semibold" />
          </div>

          <div class="col-12">
            <label class="form-label fw-semibold text-secondary" style="font-size: 0.8rem;">Job Description</label>
            <textarea :value="drive.job_description" disabled rows="5" class="form-control border border-secondary-subtle bg-light text-dark fw-semibold"></textarea>
          </div>
        </div>
      </div>

      <div class="card border border-secondary-subtle rounded-3 shadow-sm bg-white p-4">
        <div class="d-flex align-items-center gap-2 mb-4 pb-2 border-bottom">
          <div class="text-primary">
            <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" fill="currentColor" class="bi bi-shield-check" viewBox="0 0 16 16">
              <path d="M5.338 1.59a.5.5 0 0 0-.242.053L1.95 3.251A1.5 1.5 0 0 0 1 4.585v1.879c0 5.468 4.549 8.286 6.837 9.387a.5.5 0 0 0 .326 0c2.288-1.101 6.837-3.919 6.837-9.387V4.585a1.5 1.5 0 0 0-.95-1.334L10.904 1.643a.5.5 0 0 0-.568.14L8 3.48 5.338 1.59zM7.5 5.077c.48-.112.938.08 1.129.508l.18.4c.094.21.32.327.534.258l.426-.138c.45-.146.907.135.975.6l.064.44a.458.458 0 0 0 .385.385l.44.064c.465.068.746.525.6.975l-.138.426c-.069.213.048.44.258.534l.4.18c.428.19.62.649.508 1.13l-.105.45c-.105.453-.519.743-.966.623l-.443-.12c-.217-.058-.432.073-.478.291l-.096.435c-.097.442-.519.715-.96.586l-.427-.126a.46.46 0 0 0-.472.24l-.19.412c-.198.425-.662.604-1.124.475l-.439-.123a.81.81 0 0 0-.962.624l-.1.45a.5.5 0 0 1-.986-.22l.1-.45c.105-.453.519-.743.966-.623l.443.12c.217.058.432-.073.478-.291l.096-.435c.097-.442.519-.715.96-.586l.427.126a.46.46 0 0 0 .472-.24l.19-.412c.198-.425.662-.604 1.124-.475l.439.123c.447.125.869-.148.966-.59l.105-.45a1.5 1.5 0 0 0-1.524-1.85H7.5V5.077z"/>
            </svg>
          </div>
          <h5 class="fw-bold text-dark m-0">Eligibility Criteria</h5>
        </div>

        <div class="row g-3">
          <div class="col-12 col-md-6">
            <label class="form-label fw-semibold text-secondary" style="font-size: 0.8rem;">Minimum CGPA Required</label>
            <input :value="drive.min_cgpa" disabled type="text" class="form-control border border-secondary-subtle bg-light text-dark fw-semibold" />
          </div>

          <div class="col-12 col-md-6">
            <label class="form-label fw-semibold text-secondary" style="font-size: 0.8rem;">Eligible Year</label>
            <input :value="'Year ' + drive.eligible_year" disabled type="text" class="form-control border border-secondary-subtle bg-light text-dark fw-semibold" />
          </div>

          <div class="col-12">
            <label class="form-label fw-semibold text-secondary" style="font-size: 0.8rem;">Eligible Branches</label>
            <div class="d-flex flex-wrap gap-2">
              <span v-for="branch in drive.eligible_branches" :key="branch" class="badge bg-primary-subtle text-primary border border-primary-subtle px-3 py-2 fw-semibold" style="font-size: 0.85rem;">
                {{ branch }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
