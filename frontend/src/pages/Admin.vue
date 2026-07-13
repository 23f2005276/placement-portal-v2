<script setup>
import { onMounted } from 'vue';
import { useCheckIdentity } from '@/hooks/useCheckIdentity';

const props = defineProps({
  page: {
    type: String,
  },
});

const checkIdentity = useCheckIdentity()

onMounted(() => {
    checkIdentity()
})
</script>

<template>
  <div class="w-100 h-100">hello from admin</div>
</template>
