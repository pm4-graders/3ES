<script setup>
defineProps({
  msg: {
    type: String,
    required: true
  }
})
</script>

<template>
  <div class="button-container text-center">
    <div class="button-group">
      <div class="col p-3 border bg-light">
        <a href="/List">List</a>
      </div>
      <div class="col p-3 border bg-light">
        <a href="/Scanner">Scan</a>
      </div>
      <div class="col p-3 border bg-light">
        <a href="/Options">options</a>
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