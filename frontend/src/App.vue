<script setup>
import { RouterView } from 'vue-router'
import Header from './components/Header.vue'
import Navbar from './components/Navbar.vue'

console.log(1)
</script>

<template>
    <div class="container">
      <Header />
    <RouterView></RouterView>
    </div>
  <Navbar></Navbar>

</template>

<style lang="scss" scoped>

</style>
