<script setup>
import { onMounted, ref } from "vue";
import { useRoute, useRouter } from "vue-router";

const apiUrl = import.meta.env.VITE_API_BASE_URL;
const route = useRoute();
const router = useRouter();

const driveId = ref(null);
const jobTitle = ref("");
const applications = ref([]);
const errorMsg = ref("");
const successMsg = ref("");

const fetchApplications = async () => {
  const userId = localStorage.getItem("user_id");
  if (!userId) {
    errorMsg.value = "Session user ID not found. Please log in.";
    return;
  }

  const response = await fetch(`${apiUrl}/api/company_hr/drive/applications?user_id=${userId}&drive_id=${driveId.value}`, {
    method: "GET",
    credentials: "include"
  });

  if (response.ok) {
    const data = await response.json();
    jobTitle.value = data.job_title;
    applications.value = data.applications;
  } else {
    const errorData = await response.json();
    errorMsg.value = errorData.message || "Failed to load candidate applications.";
  }
};

const updateStatus = async (appId, newStatus) => {
  const userId = localStorage.getItem("user_id");
  if (!userId) return;

  const response = await fetch(`${apiUrl}/api/company_hr/drive/applications`, {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json"
    },
    credentials: "include",
    body: JSON.stringify({
      user_id: parseInt(userId),
      application_id: appId,
      status: newStatus
    })
  });

  if (response.ok) {
    successMsg.value = `Candidate application status updated to ${newStatus}.`;
    await fetchApplications();
  } else {
    const errorData = await response.json();
    errorMsg.value = errorData.message || "Failed to update status.";
  }
};

const handleBack = () => {
  router.push("/company_hr");
};

const viewStudent = (studentId) => {
  router.push(`/company_hr/drive?id=${studentId}`);
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

onMounted(async () => {
  driveId.value = route.query.drive_id;
  await fetchApplications();
});
</script>

<template>
  <div class="container-fluid py-4 font-segoe">
    <div class="row align-items-center mb-4 g-3">
      <div class="col-12 col-md-8">
        <nav aria-label="breadcrumb" style="font-size: 0.85rem;">
          <ol class="breadcrumb mb-2">
            <li class="breadcrumb-item"><span class="text-secondary" style="cursor: pointer;" @click="handleBack">Dashboard</span></li>
            <li class="breadcrumb-item active text-dark fw-semibold" aria-current="page">Applications</li>
          </ol>
        </nav>
        <h2 class="fw-bold text-dark mb-1">Applications: {{ jobTitle }}</h2>
        <p class="text-secondary m-0">Review all candidate applications submitted for this placement drive.</p>
      </div>
      <div class="col-12 col-md-4 d-flex justify-content-md-end">
        <button @click="handleBack" class="btn btn-outline-secondary px-4 fw-semibold">
          Back to Dashboard
        </button>
      </div>
    </div>

    <div v-if="errorMsg" class="alert alert-danger my-3" role="alert">
      {{ errorMsg }}
    </div>
    <div v-if="successMsg" class="alert alert-success my-3" role="alert">
      {{ successMsg }}
    </div>

    <div class="card border border-secondary-subtle rounded-3 shadow-sm bg-white p-4">
      <div class="table-responsive">
        <table class="table align-middle">
          <thead>
            <tr>
              <th class="text-secondary fw-semibold pb-3" style="font-size: 0.8rem;">STUDENT NAME</th>
              <th class="text-secondary fw-semibold pb-3" style="font-size: 0.8rem;">ROLL NUMBER</th>
              <th class="text-secondary fw-semibold pb-3" style="font-size: 0.8rem;">BRANCH</th>
              <th class="text-secondary fw-semibold pb-3" style="font-size: 0.8rem;">CGPA</th>
              <th class="text-secondary fw-semibold pb-3" style="font-size: 0.8rem;">STATUS</th>
              <th class="text-secondary fw-semibold pb-3 text-end" style="font-size: 0.8rem;">ACTIONS</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="applications.length === 0">
              <td colspan="6" class="text-center text-secondary py-4">No applications submitted for this drive yet.</td>
            </tr>
            <tr v-for="app in applications" :key="app.id">
              <td>
                <div class="fw-bold text-dark">{{ app.student_name }}</div>
              </td>
              <td>
                <div class="text-secondary fw-semibold" style="font-size: 0.9rem;">{{ app.roll_no }}</div>
              </td>
              <td>
                <div class="text-secondary fw-semibold" style="font-size: 0.9rem;">{{ app.branch_name }}</div>
              </td>
              <td>
                <div class="text-dark fw-bold" style="font-size: 0.95rem;">{{ app.cgpa }}</div>
              </td>
              <td>
                <span class="badge rounded-pill px-3 py-2 fw-semibold" :class="statusBadgeClass(app.status)" style="font-size: 0.8rem;">
                  {{ app.status.toUpperCase() }}
                </span>
              </td>
              <td class="text-end">
                <div class="d-inline-flex gap-2 align-items-center">
                  <button @click="viewStudent(app.student_id)" class="btn btn-link text-secondary p-0 border-0" title="View Details">
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-eye" viewBox="0 0 16 16">
                      <path d="M16 8s-3-5.5-8-5.5S0 8 0 8s3 5.5 8 5.5S16 8 16 8zM1.173 8a13.133 13.133 0 0 1 1.66-2.043C4.12 4.668 5.88 3.5 8 3.5c2.12 0 3.879 1.168 5.168 2.457A13.133 13.133 0 0 1 14.828 8c-.058.087-.122.183-.195.288-.335.48-.83 1.12-1.465 1.755C11.879 11.332 10.119 12.5 8 12.5c-2.12 0-3.879-1.168-5.168-2.457A13.134 13.134 0 0 1 1.172 8z"/>
                      <path d="M8 5.5a2.5 2.5 0 1 0 0 5 2.5 2.5 0 0 0 0-5zM4.5 8a3.5 3.5 0 1 1 7 0 3.5 3.5 0 0 1-7 0z"/>
                    </svg>
                  </button>

                  <button v-if="app.status === 'pending'" @click="updateStatus(app.id, 'shortlisted')" class="btn btn-sm btn-outline-primary fw-semibold px-2 py-1">
                    Shortlist
                  </button>

                  <button v-if="app.status === 'pending' || app.status === 'shortlisted'" @click="updateStatus(app.id, 'selected')" class="btn btn-sm btn-outline-success fw-semibold px-2 py-1">
                    Select
                  </button>

                  <button v-if="app.status === 'pending' || app.status === 'shortlisted'" @click="updateStatus(app.id, 'rejected')" class="btn btn-sm btn-outline-danger fw-semibold px-2 py-1">
                    Reject
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>
