<script setup>
import { onMounted, ref } from "vue";

const apiUrl = import.meta.env.VITE_API_BASE_URL;

const fullName = ref("");
const email = ref("");
const firstName = ref("");
const lastName = ref("");

const editFirstName = ref("");
const editLastName = ref("");

const fetchAdminInfo = async () => {
  const response = await fetch(`${apiUrl}/api/admin/info`, {
    method: "GET",
    credentials: "include",
  });
  if (response.ok) {
    const data = await response.json();
    if (data) {
      fullName.value = data.full_name || "";
      email.value = data.email || "";

      const parts = fullName.value.trim().split(/\s+/);
      firstName.value = parts[0] || "";
      lastName.value = parts.slice(1).join(" ") || "";

      editFirstName.value = firstName.value;
      editLastName.value = lastName.value;
    }
  }
};

const saveChanges = async () => {
  const newFullName = `${editFirstName.value} ${editLastName.value}`.trim();
  const response = await fetch(`${apiUrl}/api/admin/info`, {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
    },
    credentials: "include",
    body: JSON.stringify({ full_name: newFullName }),
  });
  if (response.ok) {
    await fetchAdminInfo();
  }
};

onMounted(async () => {
  await fetchAdminInfo();
});
</script>

<template>
  <div class="container-fluid py-4 font-segoe">
    <div class="row mb-4">
      <div class="col-12">
        <h2 class="fw-bold text-dark mb-1">Admin Profile</h2>
        <p class="text-secondary m-0">Manage your personal information and institution settings.</p>
      </div>
    </div>

    <div class="row g-4" style="max-width: 1200px;">
      <div class="col-12 col-md-4">
        <div class="card border border-secondary-subtle rounded-3 p-4 shadow-sm bg-white text-center">
          <div class="d-flex align-items-center justify-content-center mb-4">
            <div class="rounded-circle bg-light d-flex align-items-center justify-content-center border" style="width: 120px; height: 120px; font-size: 3rem; color: #6c757d; background-color: #f8f9fa !important;">
              {{ firstName.charAt(0) }}{{ lastName.charAt(0) }}
            </div>
          </div>
          <h3 class="fw-bold text-dark mb-1">{{ fullName }}</h3>
          <p class="text-primary fw-semibold mb-4" style="font-size: 0.95rem;">Placement Head</p>
          
          <hr class="text-secondary opacity-25 mb-4" />
          
          <div class="text-start d-flex align-items-start gap-3">
            <div class="text-secondary mt-1">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-envelope" viewBox="0 0 16 16">
                <path d="M0 4a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V4Zm2-1a1 1 0 0 0-1 1v.217l7 4.2 7-4.2V4a1 1 0 0 0-1-1H2Zm13 2.383-4.708 2.825L15 11.105V5.383Zm-.034 6.876-5.64-3.471L8 9.583l-1.326-.795-5.64 3.47A1 1 0 0 0 2 13h12a1 1 0 0 0 .966-.741ZM1 11.105l4.708-2.897L1 5.383v5.722Z"/>
              </svg>
            </div>
            <div>
              <div class="text-secondary fw-semibold" style="font-size: 0.85rem;">Email</div>
              <div class="text-dark fw-bold" style="font-size: 0.9rem;">{{ email }}</div>
            </div>
          </div>
        </div>
      </div>

      <div class="col-12 col-md-8">
        <div class="card border border-secondary-subtle rounded-3 shadow-sm bg-white p-4 h-100">
          <div class="d-flex align-items-center gap-2 mb-4 pb-2 border-bottom">
            <div class="text-primary">
              <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" fill="currentColor" class="bi bi-person-gear" viewBox="0 0 16 16">
                <path d="M11 5a3 3 0 1 1-6 0 3 3 0 0 1 6 0ZM8 7a2 2 0 1 0 0-4 2 2 0 0 0 0 4Zm.002 6a4.99 4.99 0 0 1 2.238-4a1.008 1.008 0 0 0 0-.083A5 5 0 0 0 2 13h6.002Zm1.896-1.44a.5.5 0 0 1-.51-.347A3.99 3.99 0 0 0 8 9c-1.96 0-3.593 1.41-3.928 3.255a.5.5 0 0 1-.497.414H2.433a.5.5 0 0 1-.49-.39C2.26 10.158 5.078 8 8 8c1.378 0 2.612.485 3.593 1.341a.5.5 0 0 1-.197.87l-.87.218a.5.5 0 0 1-.628-.868l.218-.87a.5.5 0 0 1 .868.628l-.218.87ZM14 12.5a1.5 1.5 0 1 0-3 0 1.5 1.5 0 0 0 3 0Zm-1.5 2.5a2.5 2.5 0 0 1-2.5-2.5v-3a2.5 2.5 0 0 1 5 0v3a2.5 2.5 0 0 1-2.5 2.5Z"/>
              </svg>
            </div>
            <h5 class="fw-bold text-dark m-0">Account Settings</h5>
          </div>

          <div class="row g-3">
            <div class="col-12 col-md-6">
              <label class="form-label fw-bold text-secondary" style="font-size: 0.85rem;">First Name</label>
              <input v-model="editFirstName" type="text" class="form-control" />
            </div>
            <div class="col-12 col-md-6">
              <label class="form-label fw-bold text-secondary" style="font-size: 0.85rem;">Last Name</label>
              <input v-model="editLastName" type="text" class="form-control" />
            </div>

            <div class="col-12 mt-4">
              <label class="form-label fw-bold text-secondary" style="font-size: 0.85rem;">Official Email Address</label>
              <input :value="email" type="email" class="form-control bg-light" disabled />
              <div class="form-text text-secondary mt-1" style="font-size: 0.75rem;">Contact IT support to change official email.</div>
            </div>
          </div>

          <div class="d-flex justify-content-end mt-auto pt-4">
            <button @click="saveChanges" class="btn btn-primary px-4 fw-semibold">Save Changes</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
