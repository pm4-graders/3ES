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
  },
  logo: {
    type: Boolean,
    required: true
  },
  page: {
    type: String,
    required: true
  }
})
</script>

<template>
  <nav class="navbar navbar-light bg-light">
    <a href="/" class="navbar-brand d-flex">
      <img v-if="logo" src="../assets/3ES_logo.jpg" class="logo" alt="3ES Logo Icon"/>
      <h1>{{ props.title }}</h1>
    </a>
    <h3>{{ props.page }}</h3>
  </nav>
</template>

<style scoped>
.logo {
    height: 2rem;
    width: auto;
}
</style>
