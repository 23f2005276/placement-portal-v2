<script setup>
import { onMounted, ref, computed } from "vue";
import { useRouter } from "vue-router";
import studentSignupIcon from "@/assets/svgs/studentSignupIcon.svg";
import companySignupIcon from "@/assets/svgs/companySignupIcon.svg";
import drivesIcon from "@/assets/svgs/drives.svg";

const apiUrl = import.meta.env.VITE_API_BASE_URL;
const router = useRouter();

const viewPlacementDrive = (id) => {
  router.push(`/admin/placement_drive?id=${id}`);
};

const viewUser = (user) => {
  if (user.role === "company_hr") {
    router.push(`/admin/company_hr?id=${user.id}`);
  } else {
    router.push(`/admin/student?id=${user.id}`);
  }
};

const studentsCount = ref(0);
const companiesCount = ref(0);
const drivesCount = ref(0);
const users = ref([]);
const pendingCompanies = ref([]);
const pendingDrives = ref([]);
const activeTab = ref("companies");
const searchQuery = ref("");

const filteredUsers = computed(() => {
  if (!searchQuery.value.trim()) {
    return users.value;
  }
  const query = searchQuery.value.toLowerCase().trim();
  return users.value.filter((user) => user.email && user.email.toLowerCase().includes(query));
});

const fetchUsers = async () => {
  const response = await fetch(`${apiUrl}/api/admin/users`, {
    method: "GET",
    credentials: "include",
  });
  if (response.ok) {
    const data = await response.json();
    if (data && data.users) {
      users.value = data.users;
    }
  }
};

const updateStatus = async (email, action) => {
  const response = await fetch(`${apiUrl}/api/admin/status`, {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
    },
    credentials: "include",
    body: JSON.stringify({ email, action }),
  });
  if (response.ok) {
    await fetchUsers();
  }
};

const fetchApprovals = async () => {
  const response = await fetch(`${apiUrl}/api/admin/approval`, {
    method: "GET",
    credentials: "include",
  });
  if (response.ok) {
    const data = await response.json();
    if (data) {
      pendingCompanies.value = data.pending_companies || [];
      pendingDrives.value = data.pending_drives || [];
    }
  }
};

const approveEntity = async (type, id) => {
  const response = await fetch(`${apiUrl}/api/admin/approval`, {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
    },
    credentials: "include",
    body: JSON.stringify({ type, id, action: "approve" }),
  });
  if (response.ok) {
    const data = await response.json();
    if (data) {
      pendingCompanies.value = data.pending_companies || [];
      pendingDrives.value = data.pending_drives || [];
      await fetchUsers();
    }
  }
};

const rejectEntity = async (type, id) => {
  const response = await fetch(`${apiUrl}/api/admin/approval`, {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
    },
    credentials: "include",
    body: JSON.stringify({ type, id, action: "reject" }),
  });
  if (response.ok) {
    const data = await response.json();
    if (data) {
      pendingCompanies.value = data.pending_companies || [];
      pendingDrives.value = data.pending_drives || [];
      await fetchUsers();
    }
  }
};

const statusBadgeClass = (status) => {
  if (status === "approved" || status === "active") {
    return "bg-success-subtle text-success";
  } else if (status === "pending") {
    return "bg-warning-subtle text-warning";
  } else {
    return "bg-danger-subtle text-danger";
  }
};

const formatStatus = (status) => {
  if (status === "approved" || status === "active") {
    return "Approved";
  } else if (status === "pending") {
    return "Pending";
  } else {
    return "Blacklisted";
  }
};

onMounted(async () => {
  const response = await fetch(`${apiUrl}/api/admin/total`, {
    method: "GET",
    credentials: "include",
  });
  if (response.ok) {
    const data = await response.json();
    if (data && data.total) {
      studentsCount.value = data.total.students;
      companiesCount.value = data.total.companies;
      drivesCount.value = data.total.placements;
    }
  }
  await fetchUsers();
  await fetchApprovals();
});
</script>

<template>
  <div class="container-fluid py-4 font-segoe">
    <div class="row mb-4">
      <div class="col-12">
        <h2 class="fw-bold text-dark mb-1">Admin Dashboard</h2>
        <p class="text-secondary m-0">Overview of placement activities and pending approvals.</p>
      </div>
    </div>

    <div class="row g-4 mb-4" style="max-width: 1200px;">
      <div class="col-4">
        <div class="card border border-secondary-subtle rounded-3 py-2 px-3 shadow-sm bg-white">
          <div class="d-flex ps-3 align-items-center gap-3 mb-2">
            <div class="p-2 bg-primary-subtle rounded-3 text-primary d-flex align-items-center justify-content-center">
              <img :src="studentSignupIcon" alt="" style="width: 24px; height: 24px;" />
            </div>
            <div class="fw-semibold text-secondary" style="font-size: 0.85rem;">Total Students</div>
          </div>
          <div class="text-center py-0">
            <div class="fs-1 fw-bold text-dark">{{ studentsCount.toLocaleString() }}</div>
          </div>
        </div>
      </div>

      <div class="col-4">
        <div class="card border border-secondary-subtle rounded-3 py-2 px-3 shadow-sm bg-white">
          <div class="d-flex ps-3 align-items-center gap-3 mb-2">
            <div class="p-2 bg-success-subtle rounded-3 text-success d-flex align-items-center justify-content-center">
              <img :src="companySignupIcon" alt="" style="width: 24px; height: 24px;" />
            </div>
            <div class="fw-semibold text-secondary" style="font-size: 0.85rem;">Total Companies</div>
          </div>
          <div class="text-center py-0">
            <div class="fs-1 fw-bold text-dark">{{ companiesCount.toLocaleString() }}</div>
          </div>
        </div>
      </div>

      <div class="col-4">
        <div class="card border border-secondary-subtle rounded-3 py-2 px-3 shadow-sm bg-white">
          <div class="d-flex ps-3 align-items-center gap-3 mb-2">
            <div class="p-2 bg-info-subtle rounded-3 text-info d-flex align-items-center justify-content-center">
              <img :src="drivesIcon" alt="" style="width: 24px; height: 24px; filter: invert(0.3) sepia(1) saturate(3) hue-rotate(180deg);" />
            </div>
            <div class="fw-semibold text-secondary" style="font-size: 0.85rem;">Total Placement Drives</div>
          </div>
          <div class="text-center py-0">
            <div class="fs-1 fw-bold text-dark">{{ drivesCount.toLocaleString() }}</div>
          </div>
        </div>
      </div>
    </div>

    <div class="row g-4" style="max-width: 1200px;">
      <div class="col-8">
        <div class="card border border-secondary-subtle rounded-3 shadow-sm bg-white p-3 h-100">
          <div class="d-flex justify-content-between align-items-center mb-3">
            <h5 class="fw-bold text-dark m-0">Managed Users</h5>
            <div class="input-group" style="max-width: 200px;">
              <span class="input-group-text bg-white border-end-0 text-secondary py-1 px-2">
                <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" fill="currentColor" class="bi bi-search" viewBox="0 0 16 16">
                  <path d="M11.742 10.344a6.5 6.5 0 1 0-1.397 1.398h-.001c.03.04.062.078.098.115l3.85 3.85a1 1 0 0 0 1.415-1.414l-3.85-3.85a1.007 1.007 0 0 0-.115-.1zM12 6.5a5.5 5.5 0 1 1-11 0 5.5 5.5 0 0 1 11 0z"/>
                </svg>
              </span>
              <input v-model="searchQuery" type="text" class="form-control border-start-0 ps-0 py-1" placeholder="Filter by email" style="font-size: 0.8rem;" />
            </div>
          </div>
          <div class="table-responsive" style="max-height: 250px; overflow-y: auto;">
            <table class="table align-middle m-0">
              <thead class="table-light sticky-top">
                <tr style="font-size: 0.8rem;">
                  <th scope="col" class="py-2 px-3 text-secondary fw-semibold">Entity Name</th>
                  <th scope="col" class="py-2 px-3 text-secondary fw-semibold">Type</th>
                  <th scope="col" class="py-2 px-3 text-secondary fw-semibold">Status</th>
                  <th scope="col" class="py-2 px-3 text-secondary fw-semibold">Email</th>
                  <th scope="col" class="py-2 ps-3 text-secondary fw-semibold text-end" style="padding-right: 28px !important;">Actions</th>
                </tr>
              </thead>
              <tbody style="font-size: 0.85rem;">
                <tr v-for="user in filteredUsers" :key="user.id">
                  <td class="py-2 px-3 fw-semibold text-dark">{{ user.full_name }}</td>
                  <td class="py-2 px-3 text-secondary">{{ user.role === 'company_hr' ? 'Company' : 'Student' }}</td>
                  <td class="py-2 px-3">
                    <span class="badge rounded-pill px-2 py-1" :class="statusBadgeClass(user.status)">
                      {{ formatStatus(user.status) }}
                    </span>
                  </td>
                  <td class="py-2 px-3 text-secondary">{{ user.email }}</td>
                   <td class="py-2 ps-3 text-end" style="padding-right: 28px !important;">
                    <div class="d-inline-flex align-items-center gap-2 justify-content-end w-100">
                      <button 
                        @click="viewUser(user)" 
                        class="btn btn-link text-secondary p-0 border-0" 
                        title="View Details"
                      >
                        <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="currentColor" class="bi bi-eye" viewBox="0 0 16 16">
                          <path d="M16 8s-3-5.5-8-5.5S0 8 0 8s3 5.5 8 5.5S16 8 16 8zM1.173 8a13.133 13.133 0 0 1 1.66-2.043C4.12 4.668 5.88 3.5 8 3.5c2.12 0 3.879 1.168 5.168 2.457A13.133 13.133 0 0 1 14.828 8c-.058.087-.122.183-.195.288-.335.48-.83 1.12-1.465 1.755C11.879 11.332 10.119 12.5 8 12.5c-2.12 0-3.879-1.168-5.168-2.457A13.134 13.134 0 0 1 1.172 8z"/>
                          <path d="M8 5.5a2.5 2.5 0 1 0 0 5 2.5 2.5 0 0 0 0-5zM4.5 8a3.5 3.5 0 1 1 7 0 3.5 3.5 0 0 1-7 0z"/>
                        </svg>
                      </button>
                      <button 
                        v-if="user.status === 'approved' || user.status === 'active'" 
                        @click="updateStatus(user.email, 'blacklist')" 
                        class="btn btn-link text-danger p-0 border-0" 
                        title="Blacklist User"
                      >
                        <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="currentColor" viewBox="0 0 16 16">
                          <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z"/>
                          <path d="M11.354 4.646a.5.5 0 0 0-.708 0l-6 6a.5.5 0 0 0 .708.708l6-6a.5.5 0 0 0 0-.708z"/>
                        </svg>
                      </button>
                      <button 
                        v-else 
                        @click="updateStatus(user.email, 'approve')" 
                        class="btn btn-link text-success p-0 border-0" 
                        title="Approve User"
                      >
                        <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="currentColor" viewBox="0 0 16 16">
                          <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z"/>
                          <path d="M10.97 4.97a.235.235 0 0 0-.02.022L7.477 9.417 5.384 7.323a.75.75 0 0 0-1.06 1.06L6.97 11.03a.75.75 0 0 0 1.079-.02l3.992-4.99a.75.75 0 0 0-1.071-1.05z"/>
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

      <div class="col-4">
        <div class="card border border-secondary-subtle rounded-3 shadow-sm bg-white p-3 h-100">
          <div class="d-flex align-items-center justify-content-between mb-3">
            <h5 class="fw-bold text-dark m-0">Pending Approvals</h5>
            <span class="badge bg-danger rounded-pill px-2 py-1">
              {{ pendingCompanies.length + pendingDrives.length }}
            </span>
          </div>

          <ul class="nav mb-3 border-bottom" style="font-size: 0.85rem; gap: 1rem;">
            <li class="nav-item">
              <button 
                class="nav-link border-0 bg-transparent pb-2 px-1 text-decoration-none" 
                :class="activeTab === 'companies' ? 'text-primary border-bottom border-primary fw-bold' : 'text-secondary'"
                style="border-bottom-width: 3px !important;"
                @click="activeTab = 'companies'"
              >
                Registrations
              </button>
            </li>
            <li class="nav-item">
              <button 
                class="nav-link border-0 bg-transparent pb-2 px-1 text-decoration-none" 
                :class="activeTab === 'drives' ? 'text-primary border-bottom border-primary fw-bold' : 'text-secondary'"
                style="border-bottom-width: 3px !important;"
                @click="activeTab = 'drives'"
              >
                Drives
              </button>
            </li>
          </ul>

          <div style="max-height: 250px; overflow-y: auto;">
            <div v-if="activeTab === 'companies'">
              <div v-if="pendingCompanies.length === 0" class="text-center text-secondary py-4" style="font-size: 0.85rem;">
                No pending registrations.
              </div>
              <div 
                v-else 
                v-for="company in pendingCompanies" 
                :key="company.id" 
                class="border border-secondary-subtle rounded-3 p-3 mb-2 shadow-sm bg-light"
              >
                <div class="d-flex justify-content-between align-items-start mb-2">
                  <div>
                    <div class="fw-bold text-dark" style="font-size: 0.9rem;">{{ company.company_name }}</div>
                    <div class="text-secondary" style="font-size: 0.8rem;">HR: {{ company.company_hr_name }}</div>
                  </div>
                </div>
                <div class="d-flex gap-2 mt-2">
                  <button @click="approveEntity('company', company.id)" class="btn btn-primary btn-sm flex-grow-1 py-1" style="font-size: 0.8rem;">
                    Approve
                  </button>
                </div>
              </div>
            </div>

            <div v-if="activeTab === 'drives'">
              <div v-if="pendingDrives.length === 0" class="text-center text-secondary py-4" style="font-size: 0.85rem;">
                No pending placement drives.
              </div>
              <div 
                v-else 
                v-for="drive in pendingDrives" 
                :key="drive.id" 
                class="border border-secondary-subtle rounded-3 p-3 mb-2 shadow-sm bg-light"
              >
                <div class="d-flex justify-content-between align-items-start mb-2">
                  <div>
                    <div class="fw-bold text-dark" style="font-size: 0.9rem;">{{ drive.job_title }}</div>
                    <div class="text-secondary" style="font-size: 0.8rem;">Company: {{ drive.company_name }}</div>
                  </div>
                  <button @click="viewPlacementDrive(drive.id)" class="btn btn-link text-secondary p-0 border-0" title="View Drive Details">
                    <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="currentColor" class="bi bi-eye" viewBox="0 0 16 16">
                      <path d="M16 8s-3-5.5-8-5.5S0 8 0 8s3 5.5 8 5.5S16 8 16 8zM1.173 8a13.133 13.133 0 0 1 1.66-2.043C4.12 4.668 5.88 3.5 8 3.5c2.12 0 3.879 1.168 5.168 2.457A13.133 13.133 0 0 1 14.828 8c-.058.087-.122.183-.195.288-.335.48-.83 1.12-1.465 1.755C11.879 11.332 10.119 12.5 8 12.5c-2.12 0-3.879-1.168-5.168-2.457A13.134 13.134 0 0 1 1.172 8z"/>
                      <path d="M8 5.5a2.5 2.5 0 1 0 0 5 2.5 2.5 0 0 0 0-5zM4.5 8a3.5 3.5 0 1 1 7 0 3.5 3.5 0 0 1-7 0z"/>
                    </svg>
                  </button>
                </div>
                <div class="d-flex gap-2 mt-2">
                  <button @click="approveEntity('drive', drive.id)" class="btn btn-primary btn-sm flex-grow-1 py-1" style="font-size: 0.8rem;">
                    Approve
                  </button>
                  <button @click="rejectEntity('drive', drive.id)" class="btn btn-outline-danger btn-sm flex-grow-1 py-1" style="font-size: 0.8rem;">
                    Reject
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
