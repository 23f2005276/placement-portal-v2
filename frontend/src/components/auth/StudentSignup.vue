<script setup>
import { onMounted, ref } from "vue";
import studentSignupIcon from "@/assets/svgs/studentSignupIcon.svg";
import registerIcon from "@/assets/svgs/register.svg";
import { useRouter } from "vue-router";

const apiUrl = import.meta.env.VITE_API_BASE_URL;
const router = useRouter();

const signUpForm = async (event) => {
  const form = new FormData(event.target);
  const formObject = {
    email: form.get("email"),
    password: form.get("password"),
    full_name: form.get("full_name"),
    role: "student",
    student_roll_no: form.get("student_roll_no"),
    branch: form.get("branch"),
    year_of_study: Number(form.get("year_of_study")),
    current_cgpa: Number(form.get("current_cgpa")),
  };

  fetch(`${apiUrl}/api/signup`, {
    method: "POST",
    headers: {
      "Content-type": "application/json",
    },
    body: JSON.stringify(formObject),
    credentials: "include",
  }).then(async (response) => {
    const jsonResponse = await response.json();
    if (response.ok) {
      localStorage.setItem("user_id", jsonResponse.user_id);
      router.push("/student");
    } else {
      if (typeof jsonResponse.message == "string") {
        router.push(`/Error/${response.status}/${jsonResponse.message}`);
      }
      if (typeof jsonResponse.message == "object") {
        const errorMessage = String(Object.values(jsonResponse.message)[0]);
        router.push(`/Error/${response.status}/${errorMessage}`);
      }
    }
  });
};

const branchesArray = ref([]);

onMounted(async () => {

  const data = await fetch(`${apiUrl}/api/signup?category=student`);
  const jsonData = await data.json();

  branchesArray.value = jsonData["branches_list"]["content"];
});
</script>

<template>
  <div
    class="w-100 h-100 py-2 bg-secondary-subtle text-end"
    style="padding-left: 30%; padding-right: 30%"
  >
    <div
      class="w-100 h-100 border border-secondary-subtle rounded-4 d-flex flex-column justify-content-start"
    >
      <div
        class="d-flex py-2 px-4 justify-content-start align-items-center gap-3 bg-secondary-subtle rounded-top rounded-top-4"
      >
        <img :src="studentSignupIcon" alt="" />
        <header class="font-segoe h3 text-black">Student Registration</header>
      </div>
      <form
        @submit.prevent="signUpForm"
        id="signUpFormContainer"
        class="flex-grow-1 bg-white rounded-bottom rounded-bottom-4 d-flex flex-column p-3"
      >
        <legend class="text-start fs-6 text-secondary mt-3">
          Create your account to access the Placement Portal
        </legend>
        <div class="d-flex align-items-center justify-content-between mt-4">
          <div style="width: 48%">
            <label
              for="fullName"
              class="form-label fw-semibold text-start w-100"
              style="font-size: small"
              >Full Name</label
            >
            <input
              name="full_name"
              class="form-control border-2 w-100"
              type="text"
              id="fullName"
              aria-describedby="fullNameHelp"
            />
          </div>
          <div style="width: 48%">
            <label
              for="studentRollNumber"
              class="form-label fw-semibold text-start w-100"
              style="font-size: small"
              >Student ID / Roll Number</label
            >
            <input
              name="student_roll_no"
              type="text"
              class="form-control border-2 w-100"
              id="studentRollNumber"
              aria-describedby="studentRollNumberHelp"
            />
          </div>
        </div>
        <div class="d-flex align-items-center justify-content-between mt-2">
          <div style="width: 48%">
            <label
              for="universityEmail"
              class="form-label fw-semibold text-start w-100"
              style="font-size: small"
              >University Email</label
            >
            <input
              name="email"
              type="email"
              class="form-control border-2 w-100"
              id="universityEmail"
              aria-describedby="universityEmailHelp"
            />
          </div>
          <div style="width: 48%">
            <label
              for="password"
              class="form-label fw-semibold text-start w-100"
              style="font-size: small"
              >Password</label
            >
            <input
              name="password"
              type="password"
              class="form-control border-2 w-100"
              id="password"
              aria-describedby="passwordHelp"
            />
          </div>
        </div>
        <div class="d-flex align-items-center justify-content-between mt-2">
          <div style="width: 30%">
            <label
              for="selectBranch"
              class="form-label fw-semibold text-start w-100"
              style="font-size: small"
              >Branch</label
            >
            <select
              name="branch"
              class="form-select"
              id="selectBranch"
              aria-label="Branch select"
            >
              <option selected disabled value="">Select Branch</option>
              <option
                v-for="branch in branchesArray"
                :key="branch"
                :value="branch"
              >
                {{ branch }}
              </option>
            </select>
          </div>
          <div style="width: 30%">
            <label
              for="yearOfStudy"
              class="form-label fw-semibold text-start w-100"
              style="font-size: small"
              >Year of study</label
            >
            <select
              name="year_of_study"
              class="form-select"
              id="yearOfStudy"
              aria-label="Branch select"
            >
              <option selected disabled value="">Select Year</option>
              <option value="1">1</option>
              <option value="2">2</option>
              <option value="3">3</option>
              <option value="4">4</option>
            </select>
          </div>
          <div style="width: 30%">
            <label
              for="currentCgpa"
              class="form-label fw-semibold text-start w-100"
              style="font-size: small"
              >Current CGPA</label
            >
            <!-- this any step will allow float values to get in the html -->
            <input
              name="current_cgpa"
              type="number"
              step="any"
              class="form-control"
              id="currentCgpa"
              aria-label="Current CGPA"
            />
          </div>
        </div>
        <div
          class="mt-2 flex-grow-1 d-flex justify-content-between align-items-center"
        >
          <router-link to="/login">Login Instead</router-link>
          <button
            type="submit"
            class="btn btn-primary d-flex justify-content-center align-items-center gap-2"
          >
            <span class="font-segoe fw-semibold">Register</span
            ><span
              ><img class="w-auto h-auto" :src="registerIcon" alt=""
            /></span>
          </button>
        </div>
      </form>
    </div>
  </div>
</template>
