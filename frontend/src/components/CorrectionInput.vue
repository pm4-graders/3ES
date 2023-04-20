<script setup>
import { defineProps, computed } from "vue"

const props = defineProps({
  value: {
    type: Number,
    required: false
  },
  accuracy: {
    type: Number,
    required: false
  },
})

const badgeStyle = computed(() => {
  let r = 255 * (1 - props.accuracy);
  let g = 255 * props.accuracy;
  let b = 0;
  return {
    backgroundColor: `rgb(${r}, ${g}, ${b})`
  }
})


</script>

<template>
  <div class="correction-input">
    <input class="form-control" :value="props.value">
    <div class="accuracy-badge" :style="badgeStyle" v-if="props.accuracy">Accuracy: {{ props.accuracy }}</div>
  </div>
</template>
