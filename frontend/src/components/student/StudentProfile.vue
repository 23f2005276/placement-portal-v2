<script setup>
import { onMounted, ref } from "vue";

const apiUrl = import.meta.env.VITE_API_BASE_URL;

const loading = ref(true);
const errorMsg = ref("");
const successMsg = ref("");

const name = ref("");
const email = ref("");
const password = ref("");
const rollNo = ref("");
const branch = ref("");
const yearOfStudy = ref("");
const cgpa = ref("");
const resumeFileUrl = ref("");
const skillsList = ref([]);
const newSkill = ref("");

const resumeFile = ref(null);

const fetchProfile = async () => {
  const userId = localStorage.getItem("user_id");
  if (!userId) {
    errorMsg.value = "Session user ID not found. Please log in.";
    loading.value = false;
    return;
  }

  const response = await fetch(`${apiUrl}/api/student/profile?user_id=${userId}`, {
    method: "GET",
    credentials: "include"
  });

  if (response.ok) {
    const data = await response.json();
    name.value = data.full_name;
    email.value = data.email;
    rollNo.value = data.student_roll_no;
    branch.value = data.branch;
    yearOfStudy.value = data.year_of_study;
    cgpa.value = data.current_cgpa;
    resumeFileUrl.value = data.resume_file_url;
    skillsList.value = data.skills || [];
  } else {
    const errorData = await response.json();
    errorMsg.value = errorData.message || "Failed to load student profile.";
  }
  loading.value = false;
};

const handleSaveProfile = async () => {
  errorMsg.value = "";
  successMsg.value = "";

  const userId = localStorage.getItem("user_id");
  if (!userId) return;

  const response = await fetch(`${apiUrl}/api/student/profile`, {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json"
    },
    credentials: "include",
    body: JSON.stringify({
      user_id: parseInt(userId),
      full_name: name.value,
      email: email.value,
      password: password.value,
      skills: skillsList.value
    })
  });

  if (response.ok) {
    successMsg.value = "Profile details and skills saved successfully!";
    password.value = "";
    await fetchProfile();
  } else {
    const errorData = await response.json();
    errorMsg.value = errorData.message || "Failed to update profile.";
  }
};

const handleAddSkill = () => {
  const skill = newSkill.value.trim();
  if (skill) {
    const exists = skillsList.value.some(s => s.toLowerCase() === skill.toLowerCase());
    if (!exists) {
      skillsList.value = [...skillsList.value, skill];
      newSkill.value = "";
    }
  }
};

const handleRemoveSkill = (skill) => {
  skillsList.value = skillsList.value.filter(s => s.toLowerCase() !== skill.toLowerCase());
};

const handleFileChange = (e) => {
  const selectedFile = e.target.files[0];
  if (selectedFile) {
    if (selectedFile.type !== "application/pdf") {
      errorMsg.value = "Only PDF files are allowed for resume upload.";
      resumeFile.value = null;
      return;
    }
    resumeFile.value = selectedFile;
    errorMsg.value = "";
  }
};

const handleUploadResume = async () => {
  if (!resumeFile.value) {
    errorMsg.value = "Please select a valid PDF file first.";
    return;
  }

  errorMsg.value = "";
  successMsg.value = "";

  const userId = localStorage.getItem("user_id");
  if (!userId) return;

  const formData = new FormData();
  formData.append("user_id", userId);
  formData.append("file", resumeFile.value);

  const response = await fetch(`${apiUrl}/api/student/resume/upload`, {
    method: "POST",
    credentials: "include",
    body: formData
  });

  if (response.ok) {
    successMsg.value = "Resume PDF file uploaded and updated successfully!";
    resumeFile.value = null;
    await fetchProfile();
  } else {
    const errorData = await response.json();
    errorMsg.value = errorData.message || "Failed to upload resume.";
  }
};

const getDownloadUrl = () => {
  const userId = localStorage.getItem("user_id");
  return `${apiUrl}/api/student/resume/download?user_id=${userId}&student_id=${userId}`;
};

onMounted(async () => {
  await fetchProfile();
});
</script>

<template>
  <div class="container-fluid py-4 font-segoe">
    <div class="row align-items-center mb-4 g-3">
      <div class="col-12 col-md-8">
        <h2 class="fw-bold text-dark mb-1">Student Profile</h2>
        <p class="text-secondary m-0">Manage your academic details, skills keywords, and resume files.</p>
      </div>
      <div class="col-12 col-md-4 d-flex justify-content-md-end">
        <button @click="handleSaveProfile" class="btn btn-primary px-4 fw-semibold">
          Save Changes
        </button>
      </div>
    </div>

    <div v-if="errorMsg" class="alert alert-danger my-3" role="alert">
      {{ errorMsg }}
    </div>
    <div v-if="successMsg" class="alert alert-success my-3" role="alert">
      {{ successMsg }}
    </div>

    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>

    <div v-else class="row g-4" style="max-width: 1200px;">
      <div class="col-12 col-md-8">
        <div class="card border border-secondary-subtle rounded-3 shadow-sm bg-white p-4 mb-4">
          <div class="d-flex align-items-center gap-2 mb-4 pb-2 border-bottom">
            <div class="text-primary">
              <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" fill="currentColor" class="bi bi-person" viewBox="0 0 16 16">
                <path d="M8 8a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm2-3a2 2 0 1 1-4 0 2 2 0 0 1 4 0zm4 8c0 1-1 1-1 1H3s-1 0-1-1 1-4 6-4 6 3 6 4zm-1-.004c-.001-.246-.154-.986-.832-1.664C11.516 10.68 10.289 10 8 10c-2.29 0-3.516.68-4.168 1.332-.678.678-.83 1.418-.832 1.664h10z"/>
              </svg>
            </div>
            <h5 class="fw-bold text-dark m-0">Personal & Academic Information</h5>
          </div>

          <div class="row g-3">
            <div class="col-12 col-md-6">
              <label class="form-label fw-semibold text-secondary" style="font-size: 0.8rem;">Full Name *</label>
              <input v-model="name" type="text" class="form-control border border-secondary-subtle" />
            </div>

            <div class="col-12 col-md-6">
              <label class="form-label fw-semibold text-secondary" style="font-size: 0.8rem;">Email Address *</label>
              <input v-model="email" type="email" class="form-control border border-secondary-subtle" />
            </div>

            <div class="col-12 col-md-6">
              <label class="form-label fw-semibold text-secondary" style="font-size: 0.8rem;">New Password</label>
              <input v-model="password" type="password" class="form-control border border-secondary-subtle" placeholder="Leave blank to keep unchanged" />
            </div>

            <div class="col-12 col-md-6">
              <label class="form-label fw-semibold text-secondary" style="font-size: 0.8rem;">Roll Number</label>
              <input :value="rollNo" disabled type="text" class="form-control border border-secondary-subtle bg-light text-dark fw-semibold" />
            </div>

            <div class="col-12 col-md-6">
              <label class="form-label fw-semibold text-secondary" style="font-size: 0.8rem;">Branch</label>
              <input :value="branch" disabled type="text" class="form-control border border-secondary-subtle bg-light text-dark fw-semibold" />
            </div>

            <div class="col-12 col-md-6">
              <label class="form-label fw-semibold text-secondary" style="font-size: 0.8rem;">Year of Study</label>
              <input :value="'Year ' + yearOfStudy" disabled type="text" class="form-control border border-secondary-subtle bg-light text-dark fw-semibold" />
            </div>

            <div class="col-12 col-md-6">
              <label class="form-label fw-semibold text-secondary" style="font-size: 0.8rem;">Current CGPA</label>
              <input :value="cgpa" disabled type="text" class="form-control border border-secondary-subtle bg-light text-dark fw-semibold" />
            </div>
          </div>
        </div>

        <div class="card border border-secondary-subtle rounded-3 shadow-sm bg-white p-4">
          <div class="d-flex align-items-center gap-2 mb-4 pb-2 border-bottom">
            <div class="text-primary">
              <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" fill="currentColor" class="bi bi-star" viewBox="0 0 16 16">
                <path d="M2.866 14.85c-.078.444.36.791.746.593l4.39-2.256 4.389 2.256c.386.198.824-.149.746-.592l-.83-4.73 3.522-3.356c.33-.314.16-.888-.282-.95l-4.898-.696L8.465.792a.513.513 0 0 0-.927 0L5.354 5.12l-4.898.696c-.441.062-.612.636-.283.95l3.523 3.356-.83 4.73zm4.905-2.767-3.686 1.894.694-3.957-2.928-2.79 4.008-.57 1.76-3.564 1.76 3.564 4.007.57-2.928 2.79.694 3.957-3.685-1.894z"/>
              </svg>
            </div>
            <h5 class="fw-bold text-dark m-0">Skills & Expertise</h5>
          </div>

          <div class="mb-3">
            <label class="form-label fw-semibold text-secondary" style="font-size: 0.8rem;">Add Skills Keyword</label>
            <div class="input-group" style="max-width: 400px;">
              <input v-model="newSkill" @keyup.enter="handleAddSkill" type="text" class="form-control border border-secondary-subtle" placeholder="e.g. React.js, Python, PostgreSQL" />
              <button @click="handleAddSkill" class="btn btn-outline-primary fw-semibold" type="button">
                + Add
              </button>
            </div>
          </div>

          <div class="d-flex flex-wrap gap-2 mt-3">
            <span v-for="skill in skillsList" :key="skill" class="badge bg-primary-subtle text-primary border border-primary-subtle px-3 py-2 fw-semibold d-inline-flex align-items-center gap-2" style="font-size: 0.85rem;">
              {{ skill }}
              <button @click="handleRemoveSkill(skill)" class="btn-close" style="font-size: 0.6rem;" aria-label="Remove"></button>
            </span>
          </div>
        </div>
      </div>

      <div class="col-12 col-md-4">
        <div class="card border border-secondary-subtle rounded-3 shadow-sm bg-white p-4">
          <div class="d-flex align-items-center gap-2 mb-4 pb-2 border-bottom">
            <div class="text-primary">
              <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" fill="currentColor" class="bi bi-file-earmark-arrow-up" viewBox="0 0 16 16">
                <path d="M8.5 11.5a.5.5 0 0 1-1 0V7.707L6.354 8.854a.5.5 0 1 1-.708-.708l2-2a.5.5 0 0 1 .708 0l2 2a.5.5 0 0 1-.708.708L8.5 7.707V11.5z"/>
                <path d="M14 14V4.5L9.5 0H4a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2zM9.5 3a1.5 1.5 0 0 0 1 1.5h2V14a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1h5.5v2z"/>
              </svg>
            </div>
            <h5 class="fw-bold text-dark m-0">Resume Management</h5>
          </div>

          <div v-if="resumeFileUrl" class="mb-4">
            <div class="p-3 bg-light rounded border border-secondary-subtle d-flex align-items-center justify-content-between mb-3">
              <div class="d-flex align-items-center gap-2">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-file-earmark-pdf text-danger" viewBox="0 0 16 16">
                  <path d="M14 14V4.5L9.5 0H4a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2zM9.5 3A1.5 1.5 0 0 0 11 4.5h2V14a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1h5.5v2z"/>
                </svg>
                <span class="text-secondary fw-semibold" style="font-size: 0.9rem;">{{ resumeFileUrl }}</span>
              </div>
            </div>
            <a :href="getDownloadUrl()" target="_blank" class="btn btn-outline-secondary w-100 fw-semibold">
              Download Resume
            </a>
          </div>

          <div class="border border-dashed border-secondary rounded-3 p-4 text-center bg-light mb-3">
            <label for="resume-input" style="cursor: pointer;" class="w-100">
              <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" fill="currentColor" class="bi bi-cloud-upload text-secondary mb-2" viewBox="0 0 16 16">
                <path fill-rule="evenodd" d="M7.646 5.146a.5.5 0 0 1 .708 0l2 2a.5.5 0 0 1-.708.708L8.5 6.707V10.5a.5.5 0 0 1-1 0V6.707L6.354 7.854a.5.5 0 1 1-.708-.708l2-2z"/>
                <path d="M4.406 3.342A5.53 5.53 0 0 1 8 2c2.69 0 4.923 2 5.166 4.579C14.758 6.804 16 8.137 16 9.773 16 11.569 14.502 13 12.687 13H3.781C1.708 13 0 11.366 0 9.318c0-1.763 1.266-3.223 2.942-3.593.143-.863.698-1.723 1.464-2.383zm.653.757c-.757.653-1.153 1.44-1.153 2.056v.448l-.445.049C2.064 6.805 1 7.952 1 9.318 1 10.785 2.23 12 3.781 12h8.906C13.98 12 15 10.988 15 9.773c0-1.216-1.02-2.228-2.313-2.228h-.5v-.5C12.188 4.514 10.312 3 8 3c-1.921 0-3.52 1.056-4.041 2.5a.777.777 0 0 1-.762.593.777.777 0 0 1-.762-.593A4.52 4.52 0 0 0 8 3.5c2.19 0 3.98 1.5 4.332 3.5a.5.5 0 0 1-.49.578H3.78c-1.39 0-2.52 1.085-2.52 2.422C1.26 11.458 2.27 12 3.5 12h9a2.5 2.5 0 0 0 2.5-2.5c0-1.32-1.09-2.35-2.45-2.35h-.5a.5.5 0 0 1-.5-.5c0-2.37-1.87-4-4.2-4a4.53 4.53 0 0 0-3.488 1.636z"/>
              </svg>
              <div class="fw-bold text-dark small mb-1">Click to Update Resume</div>
              <div class="text-secondary small">PDF, Max 2MB (Recommended)</div>
              <input id="resume-input" type="file" accept=".pdf" class="d-none" @change="handleFileChange" />
            </label>
          </div>

          <div v-if="resumeFile" class="mb-3 text-center small text-primary fw-semibold">
            Selected file: {{ resumeFile.name }}
          </div>

          <button @click="handleUploadResume" class="btn btn-outline-primary w-100 fw-semibold" :disabled="!resumeFile">
            Upload Selected Resume
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.border-dashed {
  border-style: dashed !important;
}
</style>
