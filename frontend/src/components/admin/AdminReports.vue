<script setup>
import { onMounted, ref } from "vue";

const apiUrl = import.meta.env.VITE_API_BASE_URL;

const loading = ref(true);
const errorMsg = ref("");
const stats = ref({
  total_students_placed: 0,
  overall_placement_rate: 0.0,
  average_package: 0.0,
  highest_package: 0.0,
  top_companies: []
});

const fetchReports = async () => {
  const response = await fetch(`${apiUrl}/api/admin/placement_reports`, {
    method: "GET",
    credentials: "include"
  });

  if (response.ok) {
    stats.value = await response.json();
  } else {
    const errorData = await response.json();
    errorMsg.value = errorData.message || "Failed to load placement reports.";
  }
  loading.value = false;
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
        <h2 class="fw-bold text-dark mb-1">Placement Reports</h2>
        <p class="text-secondary m-0">Comprehensive overview of placement statistics and trends.</p>
      </div>
      <div class="col-12 col-md-4 d-flex justify-content-md-end">
        <button @click="handleExport" class="btn btn-primary px-4 fw-semibold">
          Generate Report
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
        <div class="col-12 col-md-4">
          <div class="card border border-secondary-subtle rounded-3 shadow-sm bg-white p-4 h-100 d-flex flex-column justify-content-between">
            <div>
              <div class="text-secondary small fw-semibold mb-2">TOTAL STUDENTS PLACED</div>
              <h1 class="fw-bold text-dark mb-0">{{ stats.total_students_placed }}</h1>
            </div>
            <div class="mt-3">
              <span class="badge bg-primary-subtle text-primary border border-primary-subtle px-2 py-1">Hired Candidates</span>
            </div>
          </div>
        </div>

        <div class="col-12 col-md-4">
          <div class="card border border-secondary-subtle rounded-3 shadow-sm bg-white p-4 h-100 d-flex flex-column justify-content-between">
            <div>
              <div class="text-secondary small fw-semibold mb-2">OVERALL PLACEMENT RATE</div>
              <h1 class="fw-bold text-dark mb-0">{{ stats.overall_placement_rate }}%</h1>
            </div>
            <div class="mt-3 text-secondary small fw-semibold">
              Of Unplaced students
            </div>
          </div>
        </div>

        <div class="col-12 col-md-4">
          <div class="card border border-secondary-subtle rounded-3 shadow-sm bg-white p-4 h-100 d-flex flex-column justify-content-between">
            <div>
              <div class="text-secondary small fw-semibold mb-2">AVERAGE PACKAGE (LPA)</div>
              <h1 class="fw-bold text-dark mb-0">{{ stats.average_package }}</h1>
            </div>
            <div class="mt-3 text-secondary small fw-semibold">
              Highest: {{ stats.highest_package }} LPA
            </div>
          </div>
        </div>
      </div>

      <div class="card border border-secondary-subtle rounded-3 shadow-sm bg-white p-4" style="max-width: 1200px;">
        <div class="d-flex align-items-center justify-content-between mb-4 pb-2 border-bottom">
          <h5 class="fw-bold text-dark m-0">Top Recruiting Companies</h5>
        </div>

        <div class="table-responsive">
          <table class="table align-middle">
            <thead>
              <tr>
                <th class="text-secondary fw-semibold pb-3" style="font-size: 0.8rem;">COMPANY NAME</th>
                <th class="text-secondary fw-semibold pb-3" style="font-size: 0.8rem;">SECTOR</th>
                <th class="text-secondary fw-semibold pb-3" style="font-size: 0.8rem;">STUDENTS HIRED</th>
                <th class="text-secondary fw-semibold pb-3 text-end" style="font-size: 0.8rem;">AVG PACKAGE (LPA)</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="stats.top_companies.length === 0">
                <td colspan="4" class="text-center text-secondary py-4">No top hiring data found.</td>
              </tr>
              <tr v-for="company in stats.top_companies" :key="company.company_name">
                <td>
                  <div class="fw-bold text-dark">{{ company.company_name }}</div>
                </td>
                <td>
                  <div class="text-secondary fw-semibold" style="font-size: 0.9rem;">{{ company.sector }}</div>
                </td>
                <td>
                  <div class="text-dark fw-bold">{{ company.students_hired }}</div>
                </td>
                <td class="text-end text-secondary fw-semibold" style="font-size: 0.9rem;">
                  {{ company.avg_package }} LPA
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>
