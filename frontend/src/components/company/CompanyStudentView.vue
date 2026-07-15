<script setup>
import { onMounted, ref } from "vue";
import { useRoute, useRouter } from "vue-router";

const apiUrl = import.meta.env.VITE_API_BASE_URL;
const route = useRoute();
const router = useRouter();

const studentId = ref(null);
const student = ref(null);
const loading = ref(true);
const errorMsg = ref("");

const fetchStudentDetails = async () => {
  const userId = localStorage.getItem("user_id");
  if (!userId) {
    errorMsg.value = "Session user ID not found. Please log in.";
    loading.value = false;
    return;
  }

  const response = await fetch(`${apiUrl}/api/company_hr/student?user_id=${userId}&student_id=${studentId.value}`, {
    method: "GET",
    credentials: "include"
  });

  if (response.ok) {
    student.value = await response.json();
  } else {
    const errorData = await response.json();
    errorMsg.value = errorData.message || "Student details not found.";
  }
  loading.value = false;
};

const handleBack = () => {
  router.back();
};

onMounted(async () => {
  studentId.value = route.query.id || route.query.student_id;
  await fetchStudentDetails();
});
</script>

<template>
  <div class="container-fluid py-4 font-segoe">
    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>

    <div v-else-if="errorMsg" class="alert alert-danger" role="alert">
      {{ errorMsg }}
      <div class="mt-3">
        <button @click="handleBack" class="btn btn-secondary btn-sm">Back</button>
      </div>
    </div>

    <div v-else class="card border border-secondary-subtle rounded-3 shadow-sm bg-white p-4 mx-auto" style="max-width: 800px;">
      <div class="d-flex align-items-center justify-content-between mb-4 pb-2 border-bottom">
        <div class="d-flex align-items-center gap-2">
          <div class="text-primary">
            <svg xmlns="http://www.w3.org/2000/svg" width="26" height="26" fill="currentColor" class="bi bi-person-badge" viewBox="0 0 16 16">
              <path d="M6.5 2a.5.5 0 0 0 0 1h3a.5.5 0 0 0 0-1h-3zM11 8a3 3 0 1 1-6 0 3 3 0 0 1 6 0z"/>
              <path d="M0 4a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V4zm2-1a1 1 0 0 0-1 1v8a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V4a1 1 0 0 0-1-1H2z"/>
            </svg>
          </div>
          <h3 class="fw-bold text-dark m-0">Student Profile</h3>
        </div>
        <button @click="handleBack" class="btn btn-outline-secondary btn-sm px-3">Back</button>
      </div>

      <div class="row g-3">
        <div class="col-12 col-md-6">
          <div class="p-3 bg-light rounded border border-secondary-subtle">
            <div class="text-secondary fw-semibold mb-1" style="font-size: 0.8rem;">FULL NAME</div>
            <div class="text-dark fw-bold" style="font-size: 0.95rem;">{{ student.full_name }}</div>
          </div>
        </div>

        <div class="col-12 col-md-6">
          <div class="p-3 bg-light rounded border border-secondary-subtle">
            <div class="text-secondary fw-semibold mb-1" style="font-size: 0.8rem;">EMAIL ADDRESS</div>
            <div class="text-dark fw-bold" style="font-size: 0.95rem; word-break: break-all;">{{ student.email }}</div>
          </div>
        </div>

        <div class="col-12 col-md-6">
          <div class="p-3 bg-light rounded border border-secondary-subtle">
            <div class="text-secondary fw-semibold mb-1" style="font-size: 0.8rem;">ROLL NUMBER</div>
            <div class="text-dark fw-bold" style="font-size: 0.95rem;">{{ student.student_roll_no }}</div>
          </div>
        </div>

        <div class="col-12 col-md-6">
          <div class="p-3 bg-light rounded border border-secondary-subtle">
            <div class="text-secondary fw-semibold mb-1" style="font-size: 0.8rem;">BRANCH</div>
            <div class="text-dark fw-bold" style="font-size: 0.95rem;">{{ student.branch }}</div>
          </div>
        </div>

        <div class="col-12 col-md-6">
          <div class="p-3 bg-light rounded border border-secondary-subtle">
            <div class="text-secondary fw-semibold mb-1" style="font-size: 0.8rem;">YEAR OF STUDY</div>
            <div class="text-dark fw-bold" style="font-size: 0.95rem;">{{ student.year_of_study }}</div>
          </div>
        </div>

        <div class="col-12 col-md-6">
          <div class="p-3 bg-light rounded border border-secondary-subtle">
            <div class="text-secondary fw-semibold mb-1" style="font-size: 0.8rem;">CURRENT CGPA</div>
            <div class="text-dark fw-bold" style="font-size: 0.95rem;">{{ student.current_cgpa }}</div>
          </div>
        </div>

        <div class="col-12 mt-3">
          <div class="p-3 bg-light rounded border border-secondary-subtle">
            <div class="text-secondary fw-semibold mb-2" style="font-size: 0.8rem;">SKILLS & EXPERTISE</div>
            <div v-if="student.skills && student.skills.length > 0" class="d-flex flex-wrap gap-2">
              <span v-for="skill in student.skills" :key="skill" class="badge bg-primary-subtle text-primary border border-primary-subtle px-3 py-2 fw-semibold" style="font-size: 0.85rem;">
                {{ skill }}
              </span>
            </div>
            <div v-else class="text-secondary" style="font-size: 0.9rem;">No skills listed.</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
