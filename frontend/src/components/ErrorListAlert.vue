<script setup>
import { computed } from 'vue'
const props = defineProps({
  errorList: {
    type: Array,
    required: false
  }
})

const errorList = computed(() => {
  return props.errorList
})
</script>
<template>
  <div class="alert alert-danger" v-if="errorList" data-test="error-alert">
    <div v-for="(error, i) of errorList" :key="i">{{ error }}</div>
  </div>
</template>
