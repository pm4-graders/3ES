<script setup>
const props = defineProps({
  errorList: {
    type: Array,
    required: false
  }
})
</script>
<template>
  <div class="alert alert-danger" v-if="errorList" data-test="error-alert">
    <div v-for="error of errorList">{{ error }}</div>
  </div>
</template>
