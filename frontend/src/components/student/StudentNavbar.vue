<script setup>
import { useRoute, useRouter } from "vue-router";
import { computed } from "vue";
import dashboardIcon from "@/assets/svgs/dashboard.svg";
import profileIcon from "@/assets/svgs/profile.svg";
import drivesIcon from "@/assets/svgs/drives.svg";
import logoutIcon from "@/assets/svgs/logout.svg";

const route = useRoute();
const router = useRouter();
const apiUrl = import.meta.env.VITE_API_BASE_URL;

const activePage = computed(() => route.params.page || "dashboard");

const navigate = (page) => {
  if (page === "dashboard") {
    router.push("/student");
  } else {
    router.push(`/student/${page}`);
  }
};

const logout = () => {
  fetch(`${apiUrl}/api/logout`, {
    method: "POST",
    credentials: "include",
  }).finally(() => {
    localStorage.removeItem("user_id");
    router.push("/");
  });
};
</script>

<template>
  <div class="h-100 bg-primary d-flex flex-column text-white p-3 font-segoe justify-content-between" style="width: 15%;">
    <div>
      <div class="mb-4 text-center text-md-start">
        <h5 class="fw-bold m-0 text-white">Student Portal</h5>
      </div>
      
      <div class="d-flex flex-column gap-2">
        <button 
          @click="navigate('dashboard')" 
          class="btn text-start text-white border-0 py-2 px-3 d-flex align-items-center gap-2 w-100"
          :class="activePage === 'dashboard' ? 'bg-white text-primary' : 'text-white'"
        >
          <img :src="dashboardIcon" alt="" style="width: 20px; height: 20px; filter: invert(1);" />
          <span>Dashboard</span>
        </button>
        
        <button 
          @click="navigate('profile')" 
          class="btn text-start text-white border-0 py-2 px-3 d-flex align-items-center gap-2 w-100"
          :class="activePage === 'profile' ? 'bg-white text-primary' : 'text-white'"
        >
          <img :src="profileIcon" alt="" style="width: 20px; height: 20px; filter: invert(1);" />
          <span>Profile</span>
        </button>
        
        <button 
          @click="navigate('reports')" 
          class="btn text-start text-white border-0 py-2 px-3 d-flex align-items-center gap-2 w-100"
          :class="activePage === 'reports' ? 'bg-white text-primary' : 'text-white'"
        >
          <img :src="drivesIcon" alt="" style="width: 20px; height: 20px; filter: invert(1);" />
          <span>Reports</span>
        </button>
      </div>
    </div>
    
    <div>
      <button 
        @click="logout" 
        class="btn text-start text-white border-0 py-2 px-3 d-flex align-items-center gap-2 w-100"
      >
        <img :src="logoutIcon" alt="" style="width: 20px; height: 20px; filter: invert(1);" />
        <span>Logout</span>
      </button>
    </div>
  </div>
</template>

<style scoped>
.btn:hover {
  background-color: rgba(255, 255, 255, 0.1);
  color: white;
}
.btn.bg-white {
  background-color: white !important;
  color: var(--bs-primary) !important;
}
.btn.bg-white img {
  filter: none !important;
}
.btn.bg-white:hover {
  background-color: white !important;
  color: var(--bs-primary) !important;
}
</style>
