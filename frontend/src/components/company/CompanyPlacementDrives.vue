<script setup>
import { onMounted, ref } from "vue";
import { useRouter } from "vue-router";

const apiUrl = import.meta.env.VITE_API_BASE_URL;
const router = useRouter();

const drivesList = ref([]);
const errorMsg = ref("");
const successMsg = ref("");

const fetchDrives = async () => {
  const userId = localStorage.getItem("user_id");
  if (!userId) {
    errorMsg.value = "Session user ID not found. Please log in.";
    return;
  }

  const response = await fetch(`${apiUrl}/api/company_hr/drives`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    credentials: "include",
    body: JSON.stringify({
      user_id: parseInt(userId)
    })
  });

  if (response.ok) {
    drivesList.value = await response.json();
  } else {
    const errorData = await response.json();
    errorMsg.value = errorData.message || "Failed to load placement drives.";
  }
};
const handleCloseDrive = async (driveId) => {
  const userId = localStorage.getItem("user_id");
  if (!userId) return;

  const drive = drivesList.value.find(d => d.id === driveId);
  if (!drive || drive.status !== "approved") return;

  const response = await fetch(`${apiUrl}/api/company_hr/drives`, {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json"
    },
    credentials: "include",
    body: JSON.stringify({
      user_id: parseInt(userId),
      drive_id: driveId,
      status: "closed"
    })
  });

  if (response.ok) {
    successMsg.value = "Placement drive has been closed successfully.";
    await fetchDrives();
  } else {
    const errorData = await response.json();
    errorMsg.value = errorData.message || "Failed to close placement drive.";
  }
};

const viewApplications = (driveId) => {
  const drive = drivesList.value.find(d => d.id === driveId);
  if (drive && (drive.status === "approved" || drive.status === "closed")) {
    router.push(`/company_hr/drive/applications?drive_id=${driveId}`);
  }
};

const viewDetails = (driveId) => {
  router.push(`/company_hr/drive/details?drive_id=${driveId}`);
};

const statusBadgeClass = (status) => {
  if (status === "approved" || status === "active") {
    return "bg-success-subtle text-success";
  } else if (status === "pending") {
    return "bg-warning-subtle text-warning";
  } else if (status === "closed") {
    return "bg-secondary-subtle text-secondary";
  } else {
    return "bg-danger-subtle text-danger";
  }
};

const formatStatus = (status) => {
  if (!status) return "";
  return status.charAt(0).toUpperCase() + status.slice(1);
};

onMounted(async () => {
  await fetchDrives();
});
</script>

<template>
  <div class="container-fluid py-4 font-segoe">
    <div class="row align-items-center mb-4">
      <div class="col-12">
        <h2 class="fw-bold text-dark mb-1">Placement Drives</h2>
        <p class="text-secondary m-0">View all upcoming and historical recruitment activities.</p>
      </div>
    </div>

    <div v-if="errorMsg" class="alert alert-danger my-3" role="alert">
      {{ errorMsg }}
    </div>
    <div v-if="successMsg" class="alert alert-success my-3" role="alert">
      {{ successMsg }}
    </div>

    <div class="card border border-secondary-subtle rounded-3 shadow-sm bg-white p-4">
      <div class="d-flex align-items-center justify-content-between mb-4 pb-2 border-bottom">
        <h5 class="fw-bold text-dark m-0">Recent Drives</h5>
      </div>

      <div class="table-responsive">
        <table class="table align-middle">
          <thead>
            <tr>
              <th class="text-secondary fw-semibold pb-3" style="font-size: 0.8rem;">JOB TITLE</th>
              <th class="text-secondary fw-semibold pb-3" style="font-size: 0.8rem;">APPLICANTS</th>
              <th class="text-secondary fw-semibold pb-3" style="font-size: 0.8rem;">STATUS</th>
              <th class="text-secondary fw-semibold pb-3 text-end" style="font-size: 0.8rem;">ACTIONS</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="drivesList.length === 0">
              <td colspan="4" class="text-center text-secondary py-4">No placement drives created yet.</td>
            </tr>
            <tr v-for="drive in drivesList" :key="drive.id">
              <td>
                <div class="fw-bold text-dark">
                  {{ drive.job_title }}
                </div>
              </td>
              <td>
                <div class="text-dark fw-bold">{{ drive.applicants_count }}</div>
              </td>
              <td>
                <span class="badge rounded-pill px-3 py-2 fw-semibold" :class="statusBadgeClass(drive.status)" style="font-size: 0.8rem;">
                  {{ formatStatus(drive.status) }}
                </span>
              </td>
              <td class="text-end">
                <div class="d-inline-flex gap-3 align-items-center">
                  <button 
                    @click="viewDetails(drive.id)" 
                    class="btn btn-link text-secondary p-0 border-0" 
                    title="View Details"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-file-text" viewBox="0 0 16 16">
                      <path d="M5 4a.5.5 0 0 0 0 1h6a.5.5 0 0 0 0-1H5zm-.5 2.5A.5.5 0 0 1 5 6h6a.5.5 0 0 1 0 1H5a.5.5 0 0 1-.5-.5zM5 8a.5.5 0 0 0 0 1h6a.5.5 0 0 0 0-1H5zm0 2a.5.5 0 0 0 0 1h3a.5.5 0 0 0 0-1H5z"/>
                      <path d="M2 2a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V2zm10-1H4a1 1 0 0 0-1 1v12a1 1 0 0 0 1 1h8a1 1 0 0 0 1-1V2a1 1 0 0 0-1-1z"/>
                    </svg>
                  </button>

                  <button 
                    v-if="drive.status === 'approved' || drive.status === 'closed'" 
                    @click="viewApplications(drive.id)" 
                    class="btn btn-link text-secondary p-0 border-0" 
                    title="View Applications"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="currentColor" class="bi bi-eye" viewBox="0 0 16 16">
                      <path d="M16 8s-3-5.5-8-5.5S0 8 0 8s3 5.5 8 5.5S16 8 16 8zM1.173 8a13.133 13.133 0 0 1 1.66-2.043C4.12 4.668 5.88 3.5 8 3.5c2.12 0 3.879 1.168 5.168 2.457A13.133 13.133 0 0 1 14.828 8c-.058.087-.122.183-.195.288-.335.48-.83 1.12-1.465 1.755C11.879 11.332 10.119 12.5 8 12.5c-2.12 0-3.879-1.168-5.168-2.457A13.134 13.134 0 0 1 1.172 8z"/>
                      <path d="M8 5.5a2.5 2.5 0 1 0 0 5 2.5 2.5 0 0 0 0-5zM4.5 8a3.5 3.5 0 1 1 7 0 3.5 3.5 0 0 1-7 0z"/>
                    </svg>
                  </button>

                  <button 
                    v-if="drive.status === 'approved'" 
                    @click="handleCloseDrive(drive.id)" 
                    class="btn btn-link text-secondary p-0 border-0" 
                    title="Close Drive"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-stop-circle" viewBox="0 0 16 16">
                      <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z"/>
                      <path d="M5 6.5A1.5 1.5 0 0 1 6.5 5h3A1.5 1.5 0 0 1 11 6.5v3A1.5 1.5 0 0 1 9.5 11h-3A1.5 1.5 0 0 1 5 9.5v-3z"/>
                    </svg>
                  </button>
                  <span v-else class="text-secondary opacity-50">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-x-circle" viewBox="0 0 16 16">
                      <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z"/>
                      <path d="M4.646 4.646a.5.5 0 0 1 .708 0L8 7.293l2.646-2.647a.5.5 0 0 1 .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707l-2.646 2.647a.5.5 0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 0 1 0-.708z"/>
                    </svg>
                  </span>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>
