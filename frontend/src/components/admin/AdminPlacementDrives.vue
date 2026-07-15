<script setup>
import { onMounted, ref, computed } from "vue";
import { useRouter } from "vue-router";

const apiUrl = import.meta.env.VITE_API_BASE_URL;
const router = useRouter();

const drivesList = ref([]);
const currentFilter = ref("all");
const loading = ref(true);
const errorMsg = ref("");
const successMsg = ref("");

const fetchDrives = async () => {
  const response = await fetch(`${apiUrl}/api/admin/drives`, {
    method: "GET",
    credentials: "include"
  });

  if (response.ok) {
    drivesList.value = await response.json();
  } else {
    const errorData = await response.json();
    errorMsg.value = errorData.message || "Failed to load placement drives.";
  }
  loading.value = false;
};

const handleAction = async (driveId, actionType) => {
  errorMsg.value = "";
  successMsg.value = "";

  const response = await fetch(`${apiUrl}/api/admin/drives`, {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json"
    },
    credentials: "include",
    body: JSON.stringify({
      drive_id: driveId,
      action: actionType
    })
  });

  if (response.ok) {
    successMsg.value = `Placement drive has been successfully ${actionType}d.`;
    await fetchDrives();
  } else {
    const errorData = await response.json();
    errorMsg.value = errorData.message || "Failed to update placement drive status.";
  }
};

const filteredDrives = computed(() => {
  if (currentFilter.value === "all") {
    return drivesList.value;
  }
  return drivesList.value.filter(d => d.status === currentFilter.value);
});

const statusBadgeClass = (status) => {
  if (status === "approved") {
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

const viewDetails = (driveId) => {
  router.push(`/admin/placement_drive?id=${driveId}`);
};

onMounted(async () => {
  await fetchDrives();
});
</script>

<template>
  <div class="container-fluid py-4 font-segoe">
    <div class="row align-items-center mb-4">
      <div class="col-12 col-md-6">
        <h2 class="fw-bold text-dark mb-1">Placement Drives</h2>
        <p class="text-secondary m-0">Approve, reject, or monitor company recruitment activities.</p>
      </div>
      <div class="col-12 col-md-6 d-flex justify-content-md-end mt-3 mt-md-0">
        <div class="btn-group border rounded-3 bg-white p-1" role="group">
          <button 
            v-for="filter in ['all', 'pending', 'approved', 'closed', 'rejected']" 
            :key="filter"
            @click="currentFilter = filter"
            class="btn btn-sm px-3 border-0 rounded-3 text-capitalize"
            :class="currentFilter === filter ? 'bg-primary text-white' : 'text-secondary bg-white'"
          >
            {{ filter }}
          </button>
        </div>
      </div>
    </div>

    <div v-if="errorMsg" class="alert alert-danger my-3" role="alert">
      {{ errorMsg }}
    </div>
    <div v-if="successMsg" class="alert alert-success my-3" role="alert">
      {{ successMsg }}
    </div>

    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>

    <div v-else class="card border border-secondary-subtle rounded-3 shadow-sm bg-white p-4">
      <div class="d-flex align-items-center justify-content-between mb-4 pb-2 border-bottom">
        <h5 class="fw-bold text-dark m-0">Recent Drives</h5>
      </div>

      <div class="table-responsive">
        <table class="table align-middle">
          <thead>
            <tr>
              <th class="text-secondary fw-semibold pb-3" style="font-size: 0.8rem;">COMPANY</th>
              <th class="text-secondary fw-semibold pb-3" style="font-size: 0.8rem;">JOB TITLE</th>
              <th class="text-secondary fw-semibold pb-3" style="font-size: 0.8rem;">ELIGIBILITY</th>
              <th class="text-secondary fw-semibold pb-3" style="font-size: 0.8rem;">STATUS</th>
              <th class="text-secondary fw-semibold pb-3 text-end" style="font-size: 0.8rem;">ACTIONS</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="filteredDrives.length === 0">
              <td colspan="5" class="text-center text-secondary py-4">No placement drives found under this filter.</td>
            </tr>
            <tr v-for="drive in filteredDrives" :key="drive.id">
              <td>
                <div class="fw-bold text-dark">{{ drive.company_name }}</div>
              </td>
              <td>
                <div class="text-secondary fw-semibold" style="font-size: 0.9rem;">{{ drive.job_title }}</div>
              </td>
              <td>
                <div class="text-secondary fw-semibold" style="font-size: 0.9rem;">{{ drive.eligibility_text }}</div>
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
                    <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="currentColor" class="bi bi-eye" viewBox="0 0 16 16">
                      <path d="M16 8s-3-5.5-8-5.5S0 8 0 8s3 5.5 8 5.5S16 8 16 8zM1.173 8a13.133 13.133 0 0 1 1.66-2.043C4.12 4.668 5.88 3.5 8 3.5c2.12 0 3.879 1.168 5.168 2.457A13.133 13.133 0 0 1 14.828 8c-.058.087-.122.183-.195.288-.335.48-.83 1.12-1.465 1.755C11.879 11.332 10.119 12.5 8 12.5c-2.12 0-3.879-1.168-5.168-2.457A13.134 13.134 0 0 1 1.172 8z"/>
                      <path d="M8 5.5a2.5 2.5 0 1 0 0 5 2.5 2.5 0 0 0 0-5zM4.5 8a3.5 3.5 0 1 1 7 0 3.5 3.5 0 0 1-7 0z"/>
                    </svg>
                  </button>

                  <button 
                    v-if="drive.status === 'pending'"
                    @click="handleAction(drive.id, 'approve')" 
                    class="btn btn-link text-success p-0 border-0" 
                    title="Approve Drive"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="currentColor" class="bi bi-check-circle" viewBox="0 0 16 16">
                      <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z"/>
                      <path d="M10.97 4.97a.235.235 0 0 0-.02.022L7.477 9.417 5.384 7.323a.75.75 0 0 0-1.06 1.06L6.97 11.03a.75.75 0 0 0 1.079-.02l3.992-4.99a.75.75 0 0 0-1.071-1.05z"/>
                    </svg>
                  </button>

                  <button 
                    v-if="drive.status === 'pending'"
                    @click="handleAction(drive.id, 'reject')" 
                    class="btn btn-link text-danger p-0 border-0" 
                    title="Reject Drive"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="currentColor" class="bi bi-x-circle" viewBox="0 0 16 16">
                      <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z"/>
                      <path d="M4.646 4.646a.5.5 0 0 1 .708 0L8 7.293l2.646-2.647a.5.5 0 0 1 .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707l-2.646 2.647a.5.5 0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 0 1 0-.708z"/>
                    </svg>
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
