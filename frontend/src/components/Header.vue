<script setup>
/**
 * This Component displays the header
 */

const props = defineProps({
  /**
   * Title to show in header
   */
  title: {
    type: String,
    required: true
  }
})
</script>

<template>
  <div>
    <h3>{{ props.title }}</h3>
  </div>
</template>

<style scoped></style>
