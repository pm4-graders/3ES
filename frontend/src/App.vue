<script setup>
import { computed, ref } from 'vue'

import { RouterView, useRoute } from 'vue-router'
import HeaderComponent from './components/HeaderComponent.vue'
import NavbarComponent from './components/NavbarComponent.vue'

const logo = ref(true)
const currentRoute = computed(() => useRoute().name)
const navList = ref([
  // {
  //   title: 'List',
  //   path: '/list'
  // },
  {
    title: 'Scan',
    path: '/scanner'
  },
  {
    title: 'Korrekturen',
    path: '/corrections'
  }
])
</script>

<template>
  <div class="container-fluid" style="padding-bottom: 5rem">
    <HeaderComponent title="3ES" :logo="logo" :page="currentRoute" />
    <RouterView></RouterView>
  </div>
  <NavbarComponent :list="navList"></NavbarComponent>
</template>

<style lang="scss" scoped></style>
