<script setup>
import { onMounted, ref } from "vue";
import { useRoute, useRouter } from "vue-router";

const apiUrl = import.meta.env.VITE_API_BASE_URL;
const route = useRoute();
const router = useRouter();

const studentId = ref(null);
const student = ref(null);
const loading = ref(true);

const fetchStudentDetails = async () => {
  const response = await fetch(`${apiUrl}/api/admin/user?id=${studentId.value}`, {
    method: "GET",
    credentials: "include",
  });
  if (response.ok) {
    const data = await response.json();
    if (data && data.role === "student") {
      student.value = data;
    }
  }
  loading.value = false;
};

onMounted(async () => {
  studentId.value = route.query.id;
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

    <div v-else-if="!student" class="alert alert-danger" role="alert">
      Student details not found.
      <div class="mt-3">
        <button @click="router.push('/admin')" class="btn btn-secondary btn-sm">Back to Dashboard</button>
      </div>
    </div>

    <div v-else class="card border border-secondary-subtle rounded-3 shadow-sm bg-white p-4 mx-auto" style="max-width: 800px;">
      <div class="d-flex align-items-center gap-2 mb-2 pb-2 border-bottom">
        <div class="text-primary">
          <svg xmlns="http://www.w3.org/2000/svg" width="26" height="26" fill="currentColor" class="bi bi-person-badge" viewBox="0 0 16 16">
            <path d="M6.5 2a.5.5 0 0 0 0 1h3a.5.5 0 0 0 0-1h-3zM11 8a3 3 0 1 1-6 0 3 3 0 0 1 6 0z"/>
            <path d="M0 4a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V4zm2-1a1 1 0 0 0-1 1v8a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V4a1 1 0 0 0-1-1H2z"/>
          </svg>
        </div>
        <h3 class="fw-bold text-dark m-0">Student Profile Details</h3>
      </div>
      <p class="text-secondary mb-4" style="font-size: 0.9rem;">View student's account and academic information.</p>

      <div class="row g-3">
        <div class="col-12 col-md-6">
          <label class="form-label fw-bold text-secondary" style="font-size: 0.85rem;">Full Name</label>
          <input type="text" :value="student.full_name" class="form-control bg-light" readonly />
        </div>

        <div class="col-12 col-md-6">
          <label class="form-label fw-bold text-secondary" style="font-size: 0.85rem;">Student ID / Roll Number</label>
          <input type="text" :value="student.student_roll_no" class="form-control bg-light" readonly />
        </div>

        <div class="col-12 col-md-6">
          <label class="form-label fw-bold text-secondary" style="font-size: 0.85rem;">University Email</label>
          <input type="email" :value="student.email" class="form-control bg-light" readonly />
        </div>

        <div class="col-12 col-md-6">
          <label class="form-label fw-bold text-secondary" style="font-size: 0.85rem;">Branch</label>
          <input type="text" :value="student.branch" class="form-control bg-light" readonly />
        </div>

        <div class="col-12 col-md-6">
          <label class="form-label fw-bold text-secondary" style="font-size: 0.85rem;">Year of study</label>
          <input type="text" :value="student.year_of_study" class="form-control bg-light" readonly />
        </div>

        <div class="col-12 col-md-6">
          <label class="form-label fw-bold text-secondary" style="font-size: 0.85rem;">Current CGPA</label>
          <input type="text" :value="student.current_cgpa" class="form-control bg-light" readonly />
        </div>
      </div>

      <div class="d-flex justify-content-end mt-4 pt-3 border-top">
        <button @click="router.push('/admin')" class="btn btn-primary px-4 fw-semibold">
          Back to Dashboard
        </button>
      </div>
    </div>
  </div>
</template>
