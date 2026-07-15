<script setup>
import { useRouter } from "vue-router";

const apiUrl = import.meta.env.VITE_API_BASE_URL;
const router = useRouter();

const logout = () => {
  fetch(`${apiUrl}/api/logout`, {
    method: "POST",
    credentials: "include",
  }).finally(() => {
    localStorage.removeItem("user_id");
    router.push("/");
  });
};
</script>

<template>
  <div class="vw-100 vh-100 bg-light d-flex align-items-center justify-content-center font-segoe">
    <div class="card border border-secondary-subtle rounded-3 p-5 shadow-sm bg-white text-center" style="max-width: 450px;">
      <div class="d-flex align-items-center justify-content-center mb-4">
        <div class="p-3 bg-danger-subtle rounded-3 text-danger d-flex align-items-center justify-content-center" style="width: 70px; height: 70px;">
          <svg xmlns="http://www.w3.org/2000/svg" width="36" height="36" fill="currentColor" class="bi bi-shield-x" viewBox="0 0 16 16">
            <path d="M5.338 1.59a61.44 61.44 0 0 0-2.837.856.481.481 0 0 0-.328.39c-.554 4.157.726 7.19 2.253 9.188a10.725 10.725 0 0 0 2.287 2.233c.346.244.652.42.893.533.12.057.218.095.293.118a.55.5 0 0 0 .101.025.615.615 0 0 0 .1-.025c.076-.023.174-.061.294-.118.24-.113.547-.29.893-.533a10.726 10.726 0 0 0 2.287-2.233c1.527-1.997 2.807-5.031 2.253-9.188a.48.48 0 0 0-.328-.39c-.651-.213-1.75-.56-2.837-.855C9.552 1.29 8.531 1.067 8 1.067c-.53 0-1.552.223-2.662.493zM5.088.256C6.168-.04 7.283-.24 8-.24s1.832.2 2.912.496c1.23.336 2.52.79 3.233 1.022a1.484 1.484 0 0 1 .98 1.206c.642 4.82-.796 8.358-2.51 10.6-1.12 1.466-2.47 2.528-3.328 3.133a2.736 2.736 0 0 1-3.006 0c-.858-.605-2.208-1.667-3.328-3.133C1.196 11.084-.242 7.546.4 2.726a1.484 1.484 0 0 1 .98-1.206c.713-.23 2.003-.685 3.233-1.022z"/>
            <path d="M10.146 5.146a.5.5 0 0 1 0 .708L8.707 7.293l1.439 1.44a.5.5 0 0 1-.708.708L8 8.007 6.561 9.447a.5.5 0 1 1-.708-.708L7.293 7.293 5.854 5.854a.5.5 0 0 1 .708-.708L8 6.578l1.439-1.438a.5.5 0 0 1 .707 0z"/>
          </svg>
        </div>
      </div>

      <h3 class="fw-bold text-dark mb-2">Account Status: Blacklisted</h3>
      <p class="text-secondary mb-4 px-3" style="font-size: 0.95rem;">
        Your account has been blacklisted. You no longer have access to the placement portal.
      </p>

      <div class="d-grid gap-2">
        <button @click="logout" class="btn btn-outline-secondary py-2 fw-semibold">
          Back to Login
        </button>
      </div>
    </div>
  </div>
</template>
