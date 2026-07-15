<script setup>
import { onMounted, ref } from "vue";
import { useRoute, useRouter } from "vue-router";

const apiUrl = import.meta.env.VITE_API_BASE_URL;
const route = useRoute();
const router = useRouter();

const driveId = ref(null);
const drive = ref(null);
const loading = ref(true);

const fetchDriveDetails = async () => {
  const response = await fetch(`${apiUrl}/api/admin/drives?drive_id=${driveId.value}`, {
    method: "GET",
    credentials: "include",
  });
  if (response.ok) {
    drive.value = await response.json();
  }
  loading.value = false;
};

const approveDrive = async () => {
  if (!drive.value) return;
  const response = await fetch(`${apiUrl}/api/admin/approval`, {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
    },
    credentials: "include",
    body: JSON.stringify({ type: "drive", id: drive.value.id, action: "approve" }),
  });
  if (response.ok) {
    router.push("/admin");
  }
};

const rejectDrive = async () => {
  if (!drive.value) return;
  const response = await fetch(`${apiUrl}/api/admin/approval`, {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
    },
    credentials: "include",
    body: JSON.stringify({ type: "drive", id: drive.value.id, action: "reject" }),
  });
  if (response.ok) {
    router.push("/admin");
  }
};

onMounted(async () => {
  driveId.value = route.query.id;
  await fetchDriveDetails();
});
</script>

<template>
  <div class="container-fluid py-4 font-segoe">
    <div class="row mb-4">
      <div class="col-12">
        <h2 class="fw-bold text-dark mb-1">Placement Drive Details</h2>
        <p class="text-secondary m-0">Review details and eligibility criteria for this upcoming hiring event.</p>
      </div>
    </div>

    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>

    <div v-else-if="!drive" class="alert alert-danger" role="alert">
      Placement drive not found or has already been reviewed.
      <div class="mt-3">
        <button @click="router.push('/admin')" class="btn btn-secondary btn-sm">Back to Dashboard</button>
      </div>
    </div>

    <div v-else class="row g-4" style="max-width: 1200px;">
      <div class="col-12">
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
              <label class="form-label fw-bold text-secondary" style="font-size: 0.85rem;">Job Title</label>
              <input type="text" :value="drive.job_title" class="form-control bg-light" readonly />
            </div>

            <div class="col-12 col-md-6">
              <label class="form-label fw-bold text-secondary" style="font-size: 0.85rem;">Company Name</label>
              <input type="text" :value="drive.company_name" class="form-control bg-light" readonly />
            </div>

            <div class="col-12 col-md-6">
              <label class="form-label fw-bold text-secondary" style="font-size: 0.85rem;">Location</label>
              <div class="input-group">
                <span class="input-group-text bg-light border-end-0 text-secondary">
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-geo-alt" viewBox="0 0 16 16">
                    <path d="M12.166 8.94c-.524 1.062-1.234 2.12-1.96 3.07A31.493 31.493 0 0 1 8 14.58a31.481 31.481 0 0 1-2.206-2.57c-.726-.95-1.436-2.008-1.96-3.07C3.304 7.867 3 6.862 3 6a5 5 0 0 1 10 0c0 .862-.305 1.867-.834 2.94zM8 16s6-5.686 6-10A6 6 0 0 0 2 6c0 4.314 6 10 6 10z"/>
                    <path d="M8 8a2 2 0 1 1 0-4 2 2 0 0 1 0 4zm0 1a3 3 0 1 0 0-6 3 3 0 0 0 0 6z"/>
                  </svg>
                </span>
                <input type="text" :value="drive.location" class="form-control bg-light border-start-0 ps-0" readonly />
              </div>
            </div>

            <div class="col-12 col-md-6">
              <label class="form-label fw-bold text-secondary" style="font-size: 0.85rem;">Salary / Package (CTC)</label>
              <div class="input-group">
                <span class="input-group-text bg-light border-end-0 text-secondary">
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-cash-stack" viewBox="0 0 16 16">
                    <path d="M1 3a1 1 0 0 1 1-1h12a1 1 0 0 1 1 1H1zm7 8a2 2 0 1 0 0-4 2 2 0 0 0 0 4z"/>
                    <path d="M0 5a1 1 0 0 1 1-1h14a1 1 0 0 1 1 1v8a1 1 0 0 1-1 1H1a1 1 0 0 1-1-1V5zm3 0a2 2 0 0 1-2 2v4a2 2 0 0 1 2 2h10a2 2 0 0 1 2-2V7a2 2 0 0 1-2-2H3z"/>
                  </svg>
                </span>
                <input type="text" :value="drive.salary_package" class="form-control bg-light border-start-0 ps-0" readonly />
              </div>
            </div>

            <div class="col-12 col-md-6">
              <label class="form-label fw-bold text-secondary" style="font-size: 0.85rem;">Application Deadline</label>
              <div class="input-group">
                <span class="input-group-text bg-light border-end-0 text-secondary">
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-calendar-event" viewBox="0 0 16 16">
                    <path d="M11 6.5a.5.5 0 0 1 .5-.5h1a.5.5 0 0 1 .5.5v1a.5.5 0 0 1-.5.5h-1a.5.5 0 0 1-.5-.5v-1z"/>
                    <path d="M3.5 0a.5.5 0 0 1 .5.5V1h8V.5a.5.5 0 0 1 1 0V1h1a2 2 0 0 1 2 2v11a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V3a2 2 0 0 1 2-2h1V.5a.5.5 0 0 1 .5-.5zM1 4v10a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V4H1z"/>
                  </svg>
                </span>
                <input type="text" :value="drive.application_deadline ? new Date(drive.application_deadline).toLocaleDateString() : ''" class="form-control bg-light border-start-0 ps-0" readonly />
              </div>
            </div>

            <div class="col-12">
              <label class="form-label fw-bold text-secondary" style="font-size: 0.85rem;">Job Description</label>
              <textarea class="form-control bg-light" rows="5" :value="drive.job_description" readonly></textarea>
            </div>
          </div>
        </div>

        <div class="card border border-secondary-subtle rounded-3 shadow-sm bg-white p-4 mb-4">
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
            <div class="col-12 col-md-6">
              <label class="form-label fw-bold text-secondary" style="font-size: 0.85rem;">Minimum CGPA</label>
              <input type="text" :value="drive.min_cgpa" class="form-control bg-light" readonly />
            </div>

            <div class="col-12 col-md-6">
              <label class="form-label fw-bold text-secondary" style="font-size: 0.85rem;">Eligible Year of Study</label>
              <input type="text" :value="drive.eligible_year" class="form-control bg-light" readonly />
            </div>
          </div>
        </div>

        <div class="d-flex justify-content-end align-items-center">
          <div v-if="drive.status === 'pending'" class="d-flex gap-3">
            <button @click="rejectDrive" class="btn btn-outline-danger px-4 fw-semibold">
              Reject Drive
            </button>
            <button @click="approveDrive" class="btn btn-primary px-4 fw-semibold">
              Approve Drive
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
