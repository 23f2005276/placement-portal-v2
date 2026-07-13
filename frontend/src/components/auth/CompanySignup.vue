<script setup>
import companySignupIcon from "@/assets/svgs/companySignupIcon.svg";
import registerIcon from "@/assets/svgs/register.svg";
import { onMounted, ref } from "vue";
import { useRouter } from "vue-router";

const apiUrl = import.meta.env.VITE_API_BASE_URL;
const router = useRouter()

const signUpForm = (event) => {
  const form = new FormData(event.target);

  const formObject = {
    email: form.get("email"),
    password: form.get("password"),
    full_name: form.get("full_name"),
    role: "company_hr",
    company_name: form.get("company_name"),
    company_website: form.get("company_website"),
    company_industry: form.get("company_industry"),
    company_description: form.get("company_description"),
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
      router.push(`/company_hr`)
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

const industryTypesList = ref([]);

onMounted(async () => {
  const data = await fetch(`${apiUrl}/api/signup?category=company_hr`);
  const jsonData = await data.json();

  industryTypesList.value = jsonData["industry_list"]["content"];
});
</script>

<template>
  <div
    class="w-100 h-100 py-3 bg-secondary-subtle"
    style="padding-left: 30%; padding-right: 30%"
  >
    <div
      class="w-100 h-100 border border-secondary-subtle rounded-4 d-flex flex-column justify-content-start"
    >
      <div
        class="d-flex py-2 px-4 justify-content-start align-items-center gap-3 bg-secondary-subtle rounded-top rounded-top-4"
      >
        <img :src="companySignupIcon" alt="" />
        <header class="font-segoe h3 text-black">Company Registration</header>
      </div>
      <form
        @submit.prevent="signUpForm"
        class="flex-grow-1 bg-white rounded-bottom rounded-bottom-4 d-flex flex-column p-3"
      >
        <legend class="text-start fs-6 text-secondary mt-3">
          Create your account to access the Placement Portal
        </legend>
        <div class="d-flex align-items-center justify-content-between mt-4">
          <div style="width: 48%">
            <label
              for="companyName"
              class="form-label fw-semibold text-start w-100"
              style="font-size: small"
              >Company</label
            >
            <input
              name="company_name"
              class="form-control border-2 w-100"
              type="text"
              id="companyName"
              aria-describedby="companyNameHelp"
            />
          </div>
          <div style="width: 48%">
            <label
              for="fullName"
              class="form-label fw-semibold text-start w-100"
              style="font-size: small"
              >Company HR Name</label
            >
            <input
              name="full_name"
              type="text"
              class="form-control border-2 w-100"
              id="fullName"
              aria-describedby="companyHrNameFullNameHelp"
            />
          </div>
        </div>
        <div class="d-flex align-items-center justify-content-between mt-2">
          <div style="width: 48%">
            <label
              for="companyHrEmail"
              class="form-label fw-semibold text-start w-100"
              style="font-size: small"
              >Company HR Email</label
            >
            <input
              name="email"
              type="email"
              class="form-control border-2 w-100"
              id="companyHrEmail"
              aria-describedby="companyHrEmailHelp"
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
          <div style="width: 48%">
            <label
              for="companyWebsite"
              class="form-label fw-semibold text-start w-100"
              style="font-size: small"
              >Company Website</label
            >
            <input
              name="company_website"
              type="text"
              class="form-control border-2 w-100"
              id="companyWebsite"
              aria-describedby="companyWebsiteHelp"
            />
          </div>
          <div style="width: 48%">
            <label
              for="selectIndustryType"
              class="form-label fw-semibold text-start w-100"
              style="font-size: small"
              >Industry Type</label
            >
            <select
              name="company_industry"
              class="form-select"
              id="selectIndustryType"
              aria-label="Industry Type select"
            >
              <option selected disabled value="">Select Industry Type</option>
              <option
                v-for="industry in industryTypesList"
                :key="industry"
                :value="industry"
              >
                {{ industry }}
              </option>
            </select>
          </div>
        </div>
        <div class="d-flex align-items-center justify-content-between mt-4">
          <div style="width: 100%">
            <label
              for="companyDescription"
              class="form-label fw-semibold text-start w-100"
              style="font-size: small"
              >Company Description</label
            >
            <textarea
              name="company_description"
              class="form-control border-2 w-100"
              id="companyDescription"
              aria-describedby="companyDescriptionHelp"
            >
            </textarea>
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
