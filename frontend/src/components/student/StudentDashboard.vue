<script setup>
import { onMounted, ref, computed } from "vue";
import { useRouter } from "vue-router";

const apiUrl = import.meta.env.VITE_API_BASE_URL;
const router = useRouter();

const studentInfo = ref(null);
const eligibleDrives = ref([]);
const myApplications = ref([]);
const errorMsg = ref("");
const loading = ref(true);

const fetchDashboardData = async () => {
  const userId = localStorage.getItem("user_id");
  if (!userId) {
    errorMsg.value = "Session user ID not found. Please log in.";
    loading.value = false;
    return;
  }

  const response = await fetch(`${apiUrl}/api/student/dashboard?user_id=${userId}`, {
    method: "GET",
    credentials: "include"
  });

  if (response.ok) {
    const data = await response.json();
    studentInfo.value = data.student_info;
    eligibleDrives.value = data.eligible_drives;
    myApplications.value = data.my_applications;
  } else {
    const errorData = await response.json();
    errorMsg.value = errorData.message || "Failed to load dashboard data.";
  }
  loading.value = false;
};

const initials = computed(() => {
  if (!studentInfo.value || !studentInfo.value.full_name) return "";
  const parts = studentInfo.value.full_name.split(" ");
  return parts.map(p => p[0]).join("").toUpperCase();
});

const getDownloadUrl = (filename) => {
  const userId = localStorage.getItem("user_id");
  return `${apiUrl}/api/student/resume/download?user_id=${userId}&student_id=${userId}`;
};

const getDeadlineBadgeText = (isoString) => {
  const deadline = new Date(isoString);
  const now = new Date();
  const diffTime = deadline - now;
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
  if (diffDays <= 3 && diffDays > 0) {
    return `Closes in ${diffDays}d`;
  }
  return "New";
};

const getDeadlineBadgeClass = (isoString) => {
  const text = getDeadlineBadgeText(isoString);
  if (text.startsWith("Closes")) {
    return "bg-danger-subtle text-danger";
  }
  return "bg-warning-subtle text-warning";
};

const statusBadgeClass = (status) => {
  if (status === "selected") {
    return "bg-success-subtle text-success";
  } else if (status === "shortlisted") {
    return "bg-info-subtle text-info";
  } else if (status === "pending") {
    return "bg-warning-subtle text-warning";
  } else {
    return "bg-danger-subtle text-danger";
  }
};

const formatStatus = (status) => {
  if (!status) return "";
  return status.charAt(0).toUpperCase() + status.slice(1);
};

const navigateToProfile = () => {
  router.push("/student/profile");
};

const viewDetails = (driveId) => {
  router.push(`/student/drive?id=${driveId}`);
};

const navigateToReports = () => {
  router.push("/student/reports");
};

const formatDate = (isoString) => {
  if (!isoString) return "";
  const date = new Date(isoString);
  return date.toLocaleString();
};

onMounted(async () => {
  await fetchDashboardData();
});
</script>

<template>
  <div class="container-fluid py-4 font-segoe">
    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>

    <div v-else-if="errorMsg" class="alert alert-danger" role="alert">
      {{ errorMsg }}
    </div>

    <div v-else class="row g-4" style="max-width: 1400px;">
      <div class="col-12 col-lg-4">
        <div class="card border border-secondary-subtle rounded-3 shadow-sm bg-white p-4">
          <div class="d-flex align-items-center gap-3 mb-4">
            <div class="d-flex align-items-center justify-content-center bg-primary rounded text-white fw-bold" style="width: 60px; height: 60px; font-size: 1.5rem;">
              {{ initials }}
            </div>
            <div>
              <h4 class="fw-bold text-dark mb-0">{{ studentInfo.full_name }}</h4>
              <p class="text-secondary mb-1" style="font-size: 0.9rem;">{{ studentInfo.branch_name }}</p>
              <div class="text-primary fw-semibold" style="font-size: 0.85rem;">
                <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" fill="currentColor" class="bi bi-mortarboard-fill me-1" viewBox="0 0 16 16">
                  <path d="M8.211 2.047a.5.5 0 0 0-.422 0l-7.135 3.56a.5.5 0 0 0 0 .894L3.18 7.88a5.502 5.502 0 0 0 10.53.059L15.35 6.5a.5.5 0 0 0 0-.894L8.211 2.047z"/>
                  <path d="M4.21 9.4A6.985 6.985 0 0 0 8 10.5c1.45 0 2.783-.443 3.79-1.2l-3.37-1.685a.5.5 0 0 0-.42 0L4.21 9.4z"/>
                </svg>
                CGPA: {{ studentInfo.current_cgpa }}
              </div>
            </div>
          </div>

          <div class="mt-3">
            <button @click="navigateToProfile" class="btn btn-outline-primary fw-semibold w-100">Edit Profile</button>
          </div>
        </div>
      </div>

      <div class="col-12 col-lg-8">
        <div class="h2 fw-bold text-dark mb-1">Welcome back, {{ studentInfo.full_name }}!</div>
        <p class="text-secondary mb-4">Here is an overview of your placement journey.</p>

        <div class="card border border-secondary-subtle rounded-3 shadow-sm bg-white p-4 mb-4">
          <div class="d-flex align-items-center justify-content-between mb-4 pb-2 border-bottom">
            <div>
              <h5 class="fw-bold text-dark m-0">Available Placement Drives</h5>
              <p class="text-secondary m-0" style="font-size: 0.8rem;">Only latest new placement drives matching your eligibility rules are shown here.</p>
            </div>
          </div>

          <div class="row g-3">
            <div v-if="eligibleDrives.length === 0" class="col-12 text-center text-secondary py-4">
              No eligible placement drives available at the moment.
            </div>
            <div v-for="drive in eligibleDrives" :key="drive.id" class="col-12 col-md-6">
              <div class="card border border-secondary-subtle rounded-3 p-3 bg-white h-100 d-flex flex-column justify-content-between">
                <div>
                  <div class="d-flex align-items-start justify-content-between mb-2">
                    <h6 class="fw-bold text-dark mb-0">{{ drive.company_name }}</h6>
                    <span class="text-secondary small fw-semibold" style="font-size: 0.8rem;">
                      Deadline: {{ formatDate(drive.application_deadline) }}
                    </span>
                  </div>
                  <div class="fw-semibold text-secondary mb-2" style="font-size: 0.9rem;">{{ drive.job_title }}</div>
                  
                  <div class="d-flex gap-3 text-secondary mb-3" style="font-size: 0.8rem;">
                    <div class="d-flex align-items-center gap-1">
                      <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" fill="currentColor" class="bi bi-briefcase" viewBox="0 0 16 16">
                        <path d="M6.5 1A1.5 1.5 0 0 0 5 2.5V3H1.5A1.5 1.5 0 0 0 0 4.5v8A1.5 1.5 0 0 0 1.5 14h13a1.5 1.5 0 0 0 1.5-1.5v-8A1.5 1.5 0 0 0 14.5 3H11v-.5A1.5 1.5 0 0 0 9.5 1h-3zm0 1h3a.5.5 0 0 1 .5.5V3H6v-.5a.5.5 0 0 1 .5-.5zm1.886 6.914L15 7.151V12.5a.5.5 0 0 1-.5.5h-13a.5.5 0 0 1-.5-.5V7.15l6.614 1.764a1.5 1.5 0 0 0 .772 0zM1.5 4h13a.5.5 0 0 1 .5.5v1.616L8.129 7.948a.5.5 0 0 1-.258 0L1 6.116V4.5a.5.5 0 0 1 .5-.5z"/>
                      </svg>
                      {{ drive.salary_package }} LPA
                    </div>
                    <div class="d-flex align-items-center gap-1">
                      <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" fill="currentColor" class="bi bi-geo-alt" viewBox="0 0 16 16">
                        <path d="M12.166 8.94c-.524 1.062-1.234 2.12-1.96 3.07A31.493 31.493 0 0 1 8 14.58a31.481 31.481 0 0 1-2.206-2.57c-.726-.95-1.436-2.008-1.96-3.07C3.304 7.867 3 6.862 3 6a5 5 0 0 1 10 0c0 .862-.305 1.867-.834 2.94zM8 16s6-5.686 6-10A6 6 0 0 0 2 6c0 4.314 6 10 6 10z"/>
                        <path d="M8 8a2 2 0 1 1 0-4 2 2 0 0 1 0 4zm0 1a3 3 0 1 0 0-6 3 3 0 0 0 0 6z"/>
                      </svg>
                      {{ drive.location }}
                    </div>
                  </div>
                </div>

                <button @click="viewDetails(drive.id)" class="btn btn-outline-secondary w-100 fw-semibold btn-sm mt-2">
                  View Details
                </button>
              </div>
            </div>
          </div>
        </div>

        <div class="card border border-secondary-subtle rounded-3 shadow-sm bg-white p-4">
          <div class="d-flex align-items-center justify-content-between mb-4 pb-2 border-bottom">
            <div>
              <h5 class="fw-bold text-dark m-0">My Applications</h5>
            </div>
            <button @click="navigateToReports" class="btn btn-link text-primary p-0 border-0 fw-semibold text-decoration-none" style="font-size: 0.9rem;">
              View All
            </button>
          </div>

          <div class="table-responsive">
            <table class="table align-middle">
              <thead>
                <tr>
                  <th class="text-secondary fw-semibold pb-3" style="font-size: 0.8rem;">COMPANY</th>
                  <th class="text-secondary fw-semibold pb-3" style="font-size: 0.8rem;">DRIVE TITLE</th>
                  <th class="text-secondary fw-semibold pb-3 text-end" style="font-size: 0.8rem;">LIVE STATUS</th>
                </tr>
              </thead>
              <tbody>
                <tr v-if="myApplications.length === 0">
                  <td colspan="3" class="text-center text-secondary py-4">You haven't submitted any applications yet.</td>
                </tr>
                <tr v-for="app in myApplications" :key="app.id">
                  <td>
                    <div class="fw-bold text-dark">{{ app.company_name }}</div>
                  </td>
                  <td>
                    <div class="text-secondary fw-semibold" style="font-size: 0.9rem;">{{ app.job_title }}</div>
                  </td>
                  <td class="text-end">
                    <span class="badge rounded-pill px-3 py-2 fw-semibold" :class="statusBadgeClass(app.status)" style="font-size: 0.8rem;">
                      {{ formatStatus(app.status) }}
                    </span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
