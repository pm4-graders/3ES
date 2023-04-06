<script setup>

const props = defineProps({
  list: {
    type: String,
    required: true
  }
})
</script>

<template>
  <div class="button-container text-center">
    <div class="button-group">
      <div v-for="entry of props.list" class="col p-3 border bg-light">
        <a :href="entry.path">{{entry.title}}</a>
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
