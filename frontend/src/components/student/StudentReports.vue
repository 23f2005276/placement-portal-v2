<script setup>
import { onMounted, ref } from "vue";

const apiUrl = import.meta.env.VITE_API_BASE_URL;

const loading = ref(true);
const errorMsg = ref("");
const stats = ref({
  total_applied: 0,
  shortlisted: 0,
  placed: 0,
  rejected: 0,
  applications_history: []
});

const fetchReports = async () => {
  const userId = localStorage.getItem("user_id");
  if (!userId) {
    errorMsg.value = "Session user ID not found. Please log in.";
    loading.value = false;
    return;
  }

  const response = await fetch(`${apiUrl}/api/student/reports?user_id=${userId}`, {
    method: "GET",
    credentials: "include"
  });

  if (response.ok) {
    stats.value = await response.json();
  } else {
    const errorData = await response.json();
    errorMsg.value = errorData.message || "Failed to load reports.";
  }
  loading.value = false;
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

const handleExport = () => {
};

onMounted(async () => {
  await fetchReports();
});
</script>

<template>
  <div class="container-fluid py-4 font-segoe">
    <div class="row align-items-center mb-4 g-3">
      <div class="col-12 col-md-8">
        <h2 class="fw-bold text-dark mb-1">Placement Journey Report</h2>
        <p class="text-secondary m-0">Comprehensive analysis of your application performance and drive history.</p>
      </div>
      <div class="col-12 col-md-4 d-flex justify-content-md-end">
        <button @click="handleExport" class="btn btn-outline-primary px-4 fw-semibold">
          Export CSV
        </button>
      </div>
    </div>

    <div v-if="errorMsg" class="alert alert-danger my-3" role="alert">
      {{ errorMsg }}
    </div>

    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>

    <div v-else>
      <div class="row g-3 mb-4" style="max-width: 1200px;">
        <div class="col-12 col-sm-6 col-md-3">
          <div class="card border border-secondary-subtle rounded-3 shadow-sm bg-white p-3">
            <div class="text-secondary small fw-semibold mb-1">TOTAL APPLIED</div>
            <h3 class="fw-bold text-dark m-0">{{ stats.total_applied }}</h3>
          </div>
        </div>

        <div class="col-12 col-sm-6 col-md-3">
          <div class="card border border-secondary-subtle rounded-3 shadow-sm bg-white p-3">
            <div class="text-secondary small fw-semibold mb-1">SHORTLISTED</div>
            <h3 class="fw-bold text-dark m-0">{{ stats.shortlisted }}</h3>
          </div>
        </div>

        <div class="col-12 col-sm-6 col-md-3">
          <div class="card border border-secondary-subtle rounded-3 shadow-sm bg-white p-3">
            <div class="text-secondary small fw-semibold mb-1">OFFERS</div>
            <h3 class="fw-bold text-success m-0">{{ stats.placed }}</h3>
          </div>
        </div>

        <div class="col-12 col-sm-6 col-md-3">
          <div class="card border border-secondary-subtle rounded-3 shadow-sm bg-white p-3">
            <div class="text-secondary small fw-semibold mb-1">REJECTED</div>
            <h3 class="fw-bold text-danger m-0">{{ stats.rejected }}</h3>
          </div>
        </div>
      </div>

      <div class="card border border-secondary-subtle rounded-3 shadow-sm bg-white p-4" style="max-width: 1200px;">
        <div class="d-flex align-items-center justify-content-between mb-4 pb-2 border-bottom">
          <h5 class="fw-bold text-dark m-0">Application History</h5>
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
              <tr v-if="stats.applications_history.length === 0">
                <td colspan="3" class="text-center text-secondary py-4">No application history found.</td>
              </tr>
              <tr v-for="app in stats.applications_history" :key="app.id">
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
</template>
