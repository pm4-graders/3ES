<script setup>
const props = defineProps({
  title: {
    type: String,
    required: true
  }
})
</script>

<template>
  <div>
    <h3>{{props.title}}</h3>
  </div>
</template>

<style scoped>
</style>
