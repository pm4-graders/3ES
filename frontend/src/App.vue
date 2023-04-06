<script setup>
import { ref } from 'vue'

import { RouterView } from 'vue-router'
import Header from './components/Header.vue'
import Navbar from './components/Navbar.vue'

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
  <div class="container">
    <Header title="3ES" />
    <RouterView></RouterView>
  </div>
  <Navbar :list="navList"></Navbar>
</template>

<style lang="scss" scoped></style>
