<script setup>
import { onMounted } from "vue";
import { useCheckIdentity } from "@/hooks/useCheckIdentity";
import StudentNavbar from "@/components/student/StudentNavbar.vue";
import StudentDashboard from "@/components/student/StudentDashboard.vue";
import StudentProfile from "@/components/student/StudentProfile.vue";
import StudentReports from "@/components/student/StudentReports.vue";
import StudentDriveView from "@/components/student/StudentDriveView.vue";

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
    <StudentNavbar />
    <div class="flex-grow-1 h-100 p-4 font-segoe bg-light text-dark" style="overflow-y: auto;">
      <div v-if="!page || page === 'dashboard'">
        <StudentDashboard />
      </div>
      <div v-else-if="page === 'profile'">
        <StudentProfile />
      </div>
      <div v-else-if="page === 'reports'">
        <StudentReports />
      </div>
      <div v-else-if="page === 'drive'">
        <StudentDriveView />
      </div>
    </div>
  </div>
</template>
