<script setup>
import { onMounted, ref, computed } from "vue";
import { useRouter } from "vue-router";

const apiUrl = import.meta.env.VITE_API_BASE_URL;
const router = useRouter();

const companyName = ref("");
const companyIndustry = ref("");
const activeDrives = ref([]);
const errorMsg = ref("");

const companyInitials = computed(() => {
  if (!companyName.value) return "CO";
  const nameParts = companyName.value.trim().split(" ");
  if (nameParts.length === 1) return nameParts[0].charAt(0).toUpperCase();
  return (nameParts[0].charAt(0) + nameParts[nameParts.length - 1].charAt(0)).toUpperCase();
});

const fetchDashboardData = async () => {
  const userId = localStorage.getItem("user_id");
  if (!userId) {
    errorMsg.value = "Session user ID not found. Please log in.";
    return;
  }

  const profileResponse = await fetch(`${apiUrl}/api/company/profile?user_id=${userId}`, {
    method: "GET",
    credentials: "include"
  });

  if (profileResponse.ok) {
    const data = await profileResponse.json();
    companyName.value = data.company_name;
    companyIndustry.value = data.company_industry;
  } else {
    errorMsg.value = "Failed to load company profile info.";
    return;
  }

  const drivesResponse = await fetch(`${apiUrl}/api/company_hr/active_drives?user_id=${userId}`, {
    method: "GET",
    credentials: "include"
  });

  if (drivesResponse.ok) {
    const drivesData = await drivesResponse.json();
    activeDrives.value = drivesData;
  } else {
    errorMsg.value = "Failed to load active placement drives.";
  }
};

const handleCreateDrive = () => {
  router.push("/company_hr/create");
};

const handleEditProfile = () => {
  router.push("/company_hr/profile");
};

const handleViewCandidates = (driveId) => {
  router.push(`/company_hr/drive/applications?drive_id=${driveId}`);
};

onMounted(async () => {
  await fetchDashboardData();
});
</script>

<template>
  <div class="container-fluid py-4 font-segoe">
    <div class="row align-items-center mb-4 g-3">
      <div class="col-12 col-md-8">
        <h2 class="fw-bold text-dark mb-1">Company Dashboard</h2>
        <p class="text-secondary m-0">Welcome back. Here's an overview of your recruitment activities.</p>
      </div>
      <div class="col-12 col-md-4 d-flex justify-content-md-end">
        <button @click="handleCreateDrive" class="btn btn-primary px-4 py-2 fw-semibold d-flex align-items-center gap-2">
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="currentColor" class="bi bi-plus-circle" viewBox="0 0 16 16">
            <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z"/>
            <path d="M8 4a.5.5 0 0 1 .5.5v3h3a.5.5 0 0 1 0 1h-3v3a.5.5 0 0 1-1 0v-3h-3a.5.5 0 0 1 0-1h3v-3A.5.5 0 0 1 8 4z"/>
          </svg>
          Create Placement Drive
        </button>
      </div>
    </div>

    <div v-if="errorMsg" class="alert alert-danger my-3" role="alert">
      {{ errorMsg }}
    </div>

    <div class="row g-4">
      <div class="col-12 col-md-4">
        <div class="card border border-secondary-subtle rounded-3 shadow-sm bg-white p-4 text-center">
          <div class="d-flex justify-content-center mb-3">
            <div class="rounded-circle bg-primary-subtle text-primary d-flex align-items-center justify-content-center fw-bold" style="width: 80px; height: 80px; font-size: 1.8rem;">
              {{ companyInitials }}
            </div>
          </div>
          <h4 class="fw-bold text-dark mb-1">{{ companyName }}</h4>
          <p class="text-secondary mb-4" style="font-size: 0.9rem;">Company HR Portal</p>

          <hr class="text-secondary opacity-25 mb-4" />

          <div class="text-start mb-4">
            <div class="mb-3">
              <div class="text-secondary fw-bold mb-1" style="font-size: 0.75rem;">INDUSTRY</div>
              <div class="text-dark fw-bold" style="font-size: 0.95rem;">{{ companyIndustry }}</div>
            </div>
            <div>
              <div class="text-secondary fw-bold mb-1" style="font-size: 0.75rem;">ACTIVE PLACEMENT DRIVES</div>
              <div class="text-dark fw-bold" style="font-size: 0.95rem;">{{ activeDrives.length }}</div>
            </div>
          </div>

          <button @click="handleEditProfile" class="btn btn-outline-primary w-100 fw-semibold py-2">
            Edit Profile
          </button>
        </div>
      </div>

      <div class="col-12 col-md-8">
        <div class="card border border-secondary-subtle rounded-3 shadow-sm bg-white p-4 h-100">
          <div class="d-flex align-items-center justify-content-between mb-4 pb-2 border-bottom">
            <h5 class="fw-bold text-dark m-0">Active Placement Drives</h5>
          </div>

          <div class="table-responsive">
            <table class="table align-middle">
              <thead>
                <tr>
                  <th class="text-secondary fw-semibold pb-3" style="font-size: 0.8rem;">DRIVE TITLE</th>
                  <th class="text-secondary fw-semibold pb-3" style="font-size: 0.8rem;">ROLE</th>
                  <th class="text-secondary fw-semibold pb-3" style="font-size: 0.8rem;">APPLICANTS</th>
                  <th class="text-secondary fw-semibold pb-3 text-end" style="font-size: 0.8rem;">ACTIONS</th>
                </tr>
              </thead>
              <tbody>
                <tr v-if="activeDrives.length === 0">
                  <td colspan="4" class="text-center text-secondary py-4">No active placement drives found.</td>
                </tr>
                <tr v-for="drive in activeDrives" :key="drive.id">
                  <td>
                    <div class="fw-bold text-dark">{{ drive.job_title }}</div>
                  </td>
                  <td>
                    <div class="text-secondary fw-semibold" style="font-size: 0.9rem;">{{ drive.job_title }}</div>
                  </td>
                  <td>
                    <span class="badge rounded-pill bg-light text-primary border border-primary-subtle px-3 py-2 fw-bold" style="font-size: 0.85rem;">
                      {{ drive.applicants_count }}
                    </span>
                  </td>
                  <td class="text-end">
                    <button @click="handleViewCandidates(drive.id)" class="btn btn-sm btn-outline-primary fw-semibold px-3 py-1">
                      View Candidates
                    </button>
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
