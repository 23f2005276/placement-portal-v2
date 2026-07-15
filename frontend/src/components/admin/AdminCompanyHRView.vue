<script setup>
import { onMounted, ref } from "vue";
import { useRoute, useRouter } from "vue-router";

const apiUrl = import.meta.env.VITE_API_BASE_URL;
const route = useRoute();
const router = useRouter();

const companyHrId = ref(null);
const company = ref(null);
const loading = ref(true);

const fetchCompanyDetails = async () => {
  const response = await fetch(`${apiUrl}/api/admin/user?id=${companyHrId.value}`, {
    method: "GET",
    credentials: "include",
  });
  if (response.ok) {
    const data = await response.json();
    if (data && data.role === "company_hr") {
      company.value = data;
    }
  }
  loading.value = false;
};

onMounted(async () => {
  companyHrId.value = route.query.id;
  await fetchCompanyDetails();
});
</script>

<template>
  <div class="container-fluid py-4 font-segoe">
    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>

    <div v-else-if="!company" class="alert alert-danger" role="alert">
      Company details not found.
      <div class="mt-3">
        <button @click="router.push('/admin')" class="btn btn-secondary btn-sm">Back to Dashboard</button>
      </div>
    </div>

    <div v-else class="card border border-secondary-subtle rounded-3 shadow-sm bg-white p-4 mx-auto" style="max-width: 800px;">
      <div class="d-flex align-items-center gap-2 mb-2 pb-2 border-bottom">
        <div class="text-primary">
          <svg xmlns="http://www.w3.org/2000/svg" width="26" height="26" fill="currentColor" class="bi bi-building" viewBox="0 0 16 16">
            <path fill-rule="evenodd" d="M14.763.075A.5.5 0 0 1 15 .5v15a.5.5 0 0 1-.5.5h-3a.5.5 0 0 1-.5-.5V14h-1v1.5a.5.5 0 0 1-.5.5h-9a.5.5 0 0 1-.5-.5V10a.5.5 0 0 1 .342-.474L6 7.64V1.1a.5.5 0 0 1 .278-.447l8-4a.5.5 0 0 1 .485.022zM5 12v1.5a.5.5 0 0 1-.5.5h-3a.5.5 0 0 1-.5-.5V12h4zm0-1H1v-1.5a.5.5 0 0 1 .5-.5h3a.5.5 0 0 1 .5.5V11zm10 4V1.757l-7 3.5V15h7zM9 9h2v2H9V9zm2 3H9v2h2v-2z"/>
          </svg>
        </div>
        <h3 class="fw-bold text-dark m-0">Company Profile Details</h3>
      </div>
      <p class="text-secondary mb-4" style="font-size: 0.9rem;">View company and HR contact information.</p>

      <div class="row g-3">
        <div class="col-12 col-md-6">
          <label class="form-label fw-bold text-secondary" style="font-size: 0.85rem;">Company</label>
          <input type="text" :value="company.company_name" class="form-control bg-light" readonly />
        </div>

        <div class="col-12 col-md-6">
          <label class="form-label fw-bold text-secondary" style="font-size: 0.85rem;">Company HR Name</label>
          <input type="text" :value="company.company_hr_name" class="form-control bg-light" readonly />
        </div>

        <div class="col-12 col-md-6">
          <label class="form-label fw-bold text-secondary" style="font-size: 0.85rem;">Company HR Email</label>
          <input type="email" :value="company.company_hr_email" class="form-control bg-light" readonly />
        </div>

        <div class="col-12 col-md-6">
          <label class="form-label fw-bold text-secondary" style="font-size: 0.85rem;">Company Website</label>
          <input type="text" :value="company.company_website" class="form-control bg-light" readonly />
        </div>

        <div class="col-12 col-md-6">
          <label class="form-label fw-bold text-secondary" style="font-size: 0.85rem;">Industry Type</label>
          <input type="text" :value="company.company_industry" class="form-control bg-light" readonly />
        </div>

        <div class="col-12">
          <label class="form-label fw-bold text-secondary" style="font-size: 0.85rem;">Company Description</label>
          <textarea class="form-control bg-light" rows="4" :value="company.company_description" readonly></textarea>
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
