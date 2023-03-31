<script setup>
import { RouterView } from 'vue-router'
import HelloWorld from './components/HelloWorld.vue'

console.log(1)
</script>

<template>
    <div class="container">
      <HelloWorld />
    <RouterView></RouterView>
    </div>
  <div class="button-container text-center">
    <div class="button-group">
      <div class="col p-3 border bg-light">
        file
      </div>
      <div class="col p-3 border bg-light">
        scan
      </div>
      <div class="col p-3 border bg-light">
        settings
      </div>
    </div>

  </div>

</template>

<style lang="scss" scoped>
.button-container {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  display: flex;
  justify-content: center;
}

.button-group {
  display: flex;
  flex-direction: row;
  align-items: center;
}

</style>
