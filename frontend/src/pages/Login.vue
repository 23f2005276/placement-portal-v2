<script setup>
import authBg from "@/assets/pngs/auth/authBg.png";
import { onMounted, ref, resolveDynamicComponent } from "vue";
import { useRouter } from "vue-router";
import { errorMessages } from "vue/compiler-sfc";

const apiUrl = import.meta.env.VITE_API_BASE_URL;
const router = useRouter();

const loginUser = (event) => {
  const form = new FormData(event.target);

  const formObject = {
    email: form.get("email"),
    password: form.get("password"),
  };

  fetch(`${apiUrl}/api/login`, {
    method: "POST",
    headers: {
      "Content-type": "application/json",
    },
    body: JSON.stringify(formObject),
    credentials: "include",
  }).then(async (response) => {
    const jsonResponse = await response.json();
    if (response.ok) {
      router.push(`/${jsonResponse.role}`);
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

onMounted(() => {
  fetch(`${apiUrl}/api/identity`, {
    method: "GET",
    credentials: "include",
  }).then(async (response) => {
    const jsonResponse = await response.json();
    if (response.ok) {
      router.push(`/${jsonResponse.role}`);
    }
  });
});
</script>

<template>
  <div
    class="w-100 h-100 d-flex justify-content-between align-items-center gap-0"
  >
    <div
      class="w-50 h-100 d-flex flex-column justify-content-start align-items-center bg-primary"
      :style="{
        padding: '6rem',
        background: `url(${authBg}) center / cover no-repeat`,
      }"
    >
      <div>
        <h1 class="text-white fw-bold font-segoe">Placement Portal</h1>
      </div>
      <div>
        <p class="text-white font-segoe">
          Connecting academic excellence with corporate opportunities.
        </p>
      </div>
    </div>
    <div
      class="w-50 h-100 d-flex flex-column justify-content-start align-items-center"
      style="padding: 6rem"
    >
      <div data-purpose="Welcome Back Heading" class="w-100">
        <h1 class="fw-bold text-primary font-segoe w-100 text-center">
          Welcome Back
        </h1>
        <p class="text-black font-segoe w-100 text-center">
          Please sign in to continue to your dashboard
        </p>
      </div>

      <div
        data-purpose="Input Fields Login Form"
        class="flex-grow-1 mt-3"
        style="width: 75%"
      >
        <form @submit.prevent="loginUser">
          <div class="">
            <label
              for="exampleInputEmail1"
              class="form-label fw-semibold"
              style="font-size: medium"
              >Email address</label
            >
            <input
              name="email"
              type="email"
              class="form-control border-2"
              id="exampleInputEmail1"
              aria-describedby="emailHelp"
            />
          </div>
          <div class="mt-3">
            <label
              for="exampleInputPassword1"
              class="form-label fw-semibold"
              style="font-size: medium"
              >Password</label
            >
            <input
              name="password"
              type="password"
              class="form-control border-2"
              id="exampleInputPassword1"
            />
          </div>
          <button type="submit" class="btn btn-primary mt-4 w-100">
            Submit
          </button>
          <div class="w-100 mt-3 text-center" style="font-size: medium">
            <span>New User? </span
            ><span
              ><router-link :to="`/signup`">Register Here</router-link></span
            >
          </div>
        </form>
      </div>
    </div>
  </div>
</template>
