<script setup>
import { computed, ref } from 'vue'

import { RouterView, useRoute } from 'vue-router'
import Header from './components/Header.vue'
import Navbar from './components/Navbar.vue'

const logo = ref(true)
const currentRoute = computed(() => useRoute().name)
const navList = ref([
  {
    title: 'List',
    path: '/list'
  },
  {
    title: 'Scan',
    path: '/scanner'
  },
  {
    title: 'Settings',
    path: '/settings'
  }
])
</script>

<template>
  <div class="container-fluid" style="padding-bottom: 5rem">
    <Header title="3ES" :logo="logo" :page="currentRoute" />
    <RouterView></RouterView>
  </div>
  <Navbar :list="navList"></Navbar>
</template>

<style lang="scss" scoped></style>
