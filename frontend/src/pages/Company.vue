<script setup>
import { onMounted } from "vue";
import { useCheckIdentity } from "@/hooks/useCheckIdentity";
import CompanyNavbar from "@/components/company/CompanyNavbar.vue";
import CompanyProfile from "@/components/company/CompanyProfile.vue";
import CreatePlacementDrive from "@/components/company/CreatePlacementDrive.vue";
import CompanyDashboard from "@/components/company/CompanyDashboard.vue";
import CompanyDriveApplications from "@/components/company/CompanyDriveApplications.vue";
import CompanyStudentView from "@/components/company/CompanyStudentView.vue";
import CompanyPlacementDrives from "@/components/company/CompanyPlacementDrives.vue";
import CompanyPlacementDriveView from "@/components/company/CompanyPlacementDriveView.vue";

const props = defineProps({
  page: {
    type: String,
  },
  action: {
    type: String,
  }
});

const checkIdentity = useCheckIdentity();

onMounted(() => {
  checkIdentity();
});
</script>

<template>
  <div class="w-100 h-100 d-flex flex-row">
    <CompanyNavbar />
    <div class="flex-grow-1 h-100 p-4 font-segoe bg-light text-dark" style="overflow-y: auto;">
      <div v-if="!page || page === 'dashboard'">
        <CompanyDashboard />
      </div>
      <div v-else-if="page === 'profile'">
        <CompanyProfile />
      </div>
      <div v-else-if="page === 'drives'">
        <CompanyPlacementDrives />
      </div>
      <div v-else-if="page === 'create'">
        <CreatePlacementDrive />
      </div>
      <div v-else-if="page === 'drive' && action === 'applications'">
        <CompanyDriveApplications />
      </div>
      <div v-else-if="page === 'drive' && action === 'details'">
        <CompanyPlacementDriveView />
      </div>
      <div v-else-if="page === 'drive'">
        <CompanyStudentView />
      </div>
    </div>
  </div>
</template>
