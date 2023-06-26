<script setup>
import { defineProps, computed, defineEmits } from 'vue'

const props = defineProps({
  value: {
    type: Number,
    required: false
  },
  confidence: {
    type: Number,
    required: false
  }
})

const emit = defineEmits(['change'])

const badgeStyle = computed(() => {
  let r = 255 * (1 - props.confidence)
  let g = 255 * props.confidence
  let b = 0
  return {
    backgroundColor: `rgb(${r}, ${g}, ${b})`
  }
})

const change = (e) => {
  emit('change', e.target.value)
}

const confidence = computed(() => {
  if (!props.confidence) {
    return ''
  }

  return props.confidence.toFixed(2)
})
</script>

<template>
  <div class="correction-input">
    <input class="form-control" type="number" :value="props.value" @change="change" />
    <!-- <div class="confidence-badge" :style="badgeStyle" v-if="props.confidence"> -->
    <!--   {{ confidence }} -->
    <!-- </div> -->
  </div>
</template>
