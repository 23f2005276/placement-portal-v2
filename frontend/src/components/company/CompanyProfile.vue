<script setup>
import { onMounted, ref, computed } from "vue";

const apiUrl = import.meta.env.VITE_API_BASE_URL;

const hrName = ref("");
const hrEmail = ref("");
const companyName = ref("");
const companyWebsite = ref("");
const companyDescription = ref("");
const companyIndustry = ref("");

const editHrName = ref("");
const editHrEmail = ref("");
const editHrPassword = ref("");

const errorMsg = ref("");
const successMsg = ref("");

const hrNameInitials = computed(() => {
  if (!hrName.value) return "HR";
  const parts = hrName.value.trim().split(" ");
  if (parts.length === 1) return parts[0].charAt(0).toUpperCase();
  return (parts[0].charAt(0) + parts[parts.length - 1].charAt(0)).toUpperCase();
});

const fetchProfileData = async () => {
  const userId = localStorage.getItem("user_id");
  if (!userId) {
    errorMsg.value = "Session user ID not found. Please log in.";
    return;
  }

  const response = await fetch(`${apiUrl}/api/company/profile?user_id=${userId}`, {
    method: "GET",
    credentials: "include",
  });

  if (response.ok) {
    const data = await response.json();
    hrName.value = data.hr_name;
    hrEmail.value = data.hr_email;
    companyName.value = data.company_name;
    companyWebsite.value = data.company_website;
    companyDescription.value = data.company_description;
    companyIndustry.value = data.company_industry;

    editHrName.value = hrName.value;
    editHrEmail.value = hrEmail.value;
    editHrPassword.value = "";
  } else {
    errorMsg.value = "Failed to load company profile information.";
  }
};

const resetForm = () => {
  editHrName.value = hrName.value;
  editHrEmail.value = hrEmail.value;
  editHrPassword.value = "";
  errorMsg.value = "";
  successMsg.value = "";
};

const saveChanges = async () => {
  const userId = localStorage.getItem("user_id");
  if (!userId) {
    errorMsg.value = "Session user ID not found. Please log in.";
    return;
  }

  if (!editHrName.value.trim() || !editHrEmail.value.trim()) {
    errorMsg.value = "HR Contact Name and Email are required fields.";
    return;
  }

  const payload = {
    user_id: parseInt(userId),
    hr_name: editHrName.value.trim(),
    hr_email: editHrEmail.value.trim(),
    hr_password: editHrPassword.value
  };

  const response = await fetch(`${apiUrl}/api/company/profile`, {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json"
    },
    credentials: "include",
    body: JSON.stringify(payload)
  });

  if (response.ok) {
    await fetchProfileData();
    successMsg.value = "Changes saved successfully!";
    errorMsg.value = "";
  } else {
    const errorData = await response.json();
    errorMsg.value = errorData.message || "Failed to update profile details.";
    successMsg.value = "";
  }
};

onMounted(async () => {
  await fetchProfileData();
});
</script>

<template>
  <div class="container-fluid py-4 font-segoe">
    <div class="row align-items-center mb-4">
      <div class="col">
        <h2 class="fw-bold text-dark mb-1">Company Profile</h2>
        <p class="text-secondary m-0">Manage your corporate information and placement portal access.</p>
      </div>
    </div>

    <div v-if="errorMsg" class="alert alert-danger mb-4" role="alert">
      {{ errorMsg }}
    </div>
    <div v-if="successMsg" class="alert alert-success mb-4" role="alert">
      {{ successMsg }}
    </div>

    <div class="row g-4" style="max-width: 1200px;">
      <div class="col-12 col-md-4">
        <div class="card border border-secondary-subtle rounded-3 p-4 shadow-sm bg-white text-center">
          <div class="d-flex align-items-center justify-content-center mb-4">
            <div class="rounded-circle bg-light d-flex align-items-center justify-content-center border" style="width: 120px; height: 120px; font-size: 3rem; color: #6c757d; background-color: #f8f9fa !important;">
              {{ hrNameInitials }}
            </div>
          </div>
          <h3 class="fw-bold text-dark mb-1">{{ hrName }}</h3>
          <p class="text-primary fw-semibold mb-4" style="font-size: 0.95rem;">Company HR</p>
          
          <hr class="text-secondary opacity-25 mb-4" />
          
          <div class="text-start d-flex align-items-start gap-3 mb-3">
            <div class="text-secondary mt-1">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-envelope" viewBox="0 0 16 16">
                <path d="M0 4a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V4Zm2-1a1 1 0 0 0-1 1v.217l7 4.2 7-4.2V4a1 1 0 0 0-1-1H2Zm13 2.383-4.708 2.825L15 11.105V5.383Zm-.034 6.876-5.64-3.471L8 9.583l-1.326-.795-5.64 3.47A1 1 0 0 0 2 13h12a1 1 0 0 0 .966-.741ZM1 11.105l4.708-2.897L1 5.383v5.722Z"/>
              </svg>
            </div>
            <div>
              <div class="text-secondary fw-semibold" style="font-size: 0.85rem;">Email</div>
              <div class="text-dark fw-bold" style="font-size: 0.9rem; word-break: break-all;">{{ hrEmail }}</div>
            </div>
          </div>

        </div>
      </div>

      <div class="col-12 col-md-8">
        <div class="card border border-secondary-subtle rounded-3 shadow-sm bg-white p-4 mb-4">
          <div class="d-flex align-items-center gap-2 mb-4 pb-2 border-bottom">
            <h5 class="fw-bold text-dark m-0">Company Details <span class="text-secondary fw-normal fs-6">(no edits)</span></h5>
          </div>

          <div class="row g-3">
            <div class="col-12">
              <label class="form-label fw-semibold text-secondary" style="font-size: 0.8rem;">COMPANY NAME *</label>
              <input :value="companyName" type="text" class="form-control bg-light border border-secondary-subtle" readonly />
            </div>

            <div class="col-12 col-md-6">
              <label class="form-label fw-semibold text-secondary" style="font-size: 0.8rem;">INDUSTRY TYPE *</label>
              <input :value="companyIndustry" type="text" class="form-control bg-light border border-secondary-subtle" readonly />
            </div>

            <div class="col-12 col-md-6">
              <label class="form-label fw-semibold text-secondary" style="font-size: 0.8rem;">WEBSITE</label>
              <input :value="companyWebsite" type="text" class="form-control bg-light border border-secondary-subtle" readonly />
            </div>

            <div class="col-12">
              <label class="form-label fw-semibold text-secondary" style="font-size: 0.8rem;">COMPANY DESCRIPTION</label>
              <textarea :value="companyDescription" class="form-control bg-light border border-secondary-subtle" rows="4" readonly></textarea>
            </div>
          </div>
        </div>

        <div class="card border border-secondary-subtle rounded-3 shadow-sm bg-white p-4">
          <div class="d-flex align-items-center gap-2 mb-4 pb-2 border-bottom">
            <h5 class="fw-bold text-dark m-0">HR Contact Information</h5>
          </div>

          <div class="row g-3">
            <div class="col-12">
              <label class="form-label fw-semibold text-secondary" style="font-size: 0.8rem;">PRIMARY CONTACT NAME *</label>
              <input v-model="editHrName" type="text" class="form-control border border-secondary-subtle" />
            </div>

            <div class="col-12 col-md-6">
              <label class="form-label fw-semibold text-secondary" style="font-size: 0.8rem;">OFFICIAL EMAIL *</label>
              <input v-model="editHrEmail" type="email" class="form-control border border-secondary-subtle" />
            </div>

            <div class="col-12 col-md-6">
              <label class="form-label fw-semibold text-secondary" style="font-size: 0.8rem;">NEW PASSWORD</label>
              <input v-model="editHrPassword" type="password" class="form-control border border-secondary-subtle" placeholder="Leave blank to keep current" />
            </div>
          </div>
        </div>

        <div class="d-flex justify-content-end mt-4">
          <button @click="resetForm" class="btn btn-outline-secondary px-4 py-2 fw-semibold me-3">Cancel</button>
          <button @click="saveChanges" class="btn btn-primary px-4 py-2 fw-semibold">Save Changes</button>
        </div>
      </div>
    </div>
  </div>
</template>
