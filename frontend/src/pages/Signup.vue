<script setup>
import StudentSignup from "../components/auth/StudentSignup.vue";
import CompanySignup from "../components/auth/CompanySignup.vue";
import { useRouter } from "vue-router";
import { onMounted } from "vue";
import { useCheckIdentity } from "@/hooks/useCheckIdentity.js";

const apiUrl = import.meta.env.VITE_API_BASE_URL;

const props = defineProps({
  category: {
    type: String,
  },
});

const router = useRouter();

const redirectUser = (event) => {
  const role = String(event.target.name);

  router.push(`/signup/${role}`);
};

const checkIdentity = useCheckIdentity()

onMounted(() => {
  checkIdentity()
})
</script>

<template>
  <div class="w-100 h-100">
    <StudentSignup v-if="category == 'student'" />
    <CompanySignup v-else-if="category == 'company_hr'" />
    <div
      v-if="!category"
      class="h-100 w-100 d-flex justify-content-center align-items-center"
    >
      <div
        class="bg-secondary-subtle h-50 w-50 text-black font-segoe d-flex justify-content-around align-items-center"
      >
        <button
          name="student"
          class="btn btn-primary w-25 h-50"
          @click="redirectUser"
        >
          Signup as a Student
        </button>
        <button
          name="company_hr"
          class="btn btn-primary w-25 h-50"
          @click="redirectUser"
        >
          Signup as a Company
        </button>
      </div>
    </div>
  </div>
</template>
