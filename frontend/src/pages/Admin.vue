<script setup>
import { onMounted } from "vue";
import { useCheckIdentity } from "@/hooks/useCheckIdentity";
import AdminNavbar from "@/components/admin/AdminNavbar.vue";
import AdminDashboard from "@/components/admin/AdminDashboard.vue";
import AdminProfile from "@/components/admin/AdminProfile.vue";
import AdminPlacementDriveView from "@/components/admin/AdminPlacementDriveView.vue";
import AdminStudentView from "@/components/admin/AdminStudentView.vue";
import AdminCompanyHRView from "@/components/admin/AdminCompanyHRView.vue";
import AdminPlacementDrives from "@/components/admin/AdminPlacementDrives.vue";
import AdminReports from "@/components/admin/AdminReports.vue";

const props = defineProps({
  page: {
    type: String,
  },
});

const checkIdentity = useCheckIdentity();

onMounted(() => {
  checkIdentity();
});
</script>

<template>
  <div class="w-100 h-100 d-flex flex-row">
    <AdminNavbar />
    <div class="flex-grow-1 h-100 p-4 font-segoe bg-light text-dark" style="overflow-y: auto;">
      <div v-if="!page || page === 'dashboard'">
        <AdminDashboard />
      </div>
      <div v-else-if="page === 'profile'">
        <AdminProfile />
      </div>
      <div v-else-if="page === 'drives'">
        <AdminPlacementDrives />
      </div>
      <div v-else-if="page === 'placement_drive'">
        <AdminPlacementDriveView />
      </div>
      <div v-else-if="page === 'student'">
        <AdminStudentView />
      </div>
      <div v-else-if="page === 'company_hr'">
        <AdminCompanyHRView />
      </div>
      <div v-else-if="page === 'report'">
        <AdminReports />
      </div>
    </div>
  </div>
</template>
