<script setup>
import { RouterLink, RouterView } from 'vue-router'
import HelloWorld from './components/HelloWorld.vue'
</script>

<template>
    <div class="container">
      <HelloWorld />
    <RouterView></RouterView>
    </div>
  <div class="row">
    <div class="col">a</div>
    <div class="col">b</div>
  </div>
</template>

<style lang="scss" scoped>
</style>
