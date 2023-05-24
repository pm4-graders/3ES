<script setup>
/**
 * This Component displays the header
 */

import pkgJson from '../../package.json'

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
  <header class="navbar navbar-light bg-light app-header">
    <a href="/" class="navbar-brand app-header-link">
      <img v-if="logo" src="../assets/3ES_logo.png" class="app-logo" alt="3ES Logo Icon" />
      <div class="d-flex flex-column align-items-start">
        <h1 class="app-title">{{ props.title }}</h1>
        <small>Version: {{ pkgJson.version }}</small>
      </div>
    </a>
    <h3 class="app-page">{{ props.page }}</h3>
  </header>
</template>

<style scoped>
.app-header {
  height: 60px;
  padding: 0;
  margin-bottom: 3px;
}

.app-header-link {
  height: 100%;
}

h1 {
  font-size: 1.4rem;
  margin-bottom: 0;
}
small {
  font-size: 0.6rem;
}

.app-header a {
  display: flex;
  height: 100%;
  align-items: center;
}

.app-logo {
  height: 70%;
  margin-right: 5px;
}

.app-page {
  color: #495057;
}
</style>
