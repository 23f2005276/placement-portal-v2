<script setup>
import { useRouter } from 'vue-router';

defineProps({
    status: {
        type: String,
        default: ''
    },
    message: {
        type: String, 
        default: ''
    }
})

const router = useRouter()

const goHome = () => {
    router.push('/')
}

</script>
<template>
  <div class="w-100 h-100 d-flex align-items-center justify-content-center bg-light px-3">
    <div class="bg-white border rounded text-center p-4" style="max-width: 28rem; width: 100%;">      
      <div 
        class="rounded-circle bg-danger bg-opacity-10 text-danger d-inline-flex align-items-center justify-content-center mx-auto mb-4"
        style="width: 3.5rem; height: 3.5rem;"
      >
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" style="width: 2rem; height: 2rem;">
          <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v3.75m9-.75a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9 7.5h.008v.008H12v-.008Z" />
        </svg>
      </div>

      <h1 class="fs-4 fw-bold text-dark mb-2">
        {{ status ? `Error ${status}` : 'Something went wrong' }}
      </h1>
      
      <p class="text-secondary small mb-4" style="line-height: 1.5;">
        {{ message ? message : "An unexpected error occurred. Please return to the dashboard." }}
      </p>

      <div class="d-flex flex-column gap-2">
        <button 
          @click="goHome" 
          type="button" 
          class="btn btn-primary fw-medium px-4 py-2"
        >
          Return Home
        </button>
      </div>

    </div>
  </div>
</template>