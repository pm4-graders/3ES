<script setup>
/**
 * This component displays a loading spinner or success badge while a certain action is in progress.
 */
const props = defineProps({
  /** A boolean prop that determines whether the loading spinner should be displayed or not. */
  loading: {
    type: Boolean
  },

  /** A boolean prop that determines whether the success badge should be displayed or not. */
  successBadge: {
    type: Boolean
  }
})
</script>

<template>
  <template v-if="props.loading || props.successBadge">
    <div class="loading-block">
      <div v-if="!props.successBadge" class="spinner-wrapper">
        <div class="spinner spinner-border text-primary" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
      </div>
      <div v-if="props.successBadge" class="success-wrapper">
        <i class="fa-solid fa-circle-check fa-3x text-success"></i>
      </div>
      <!-- @slot The content that will be displayed in the component. This slot will be displayed together with the loading spinner or success badge if either of them is enabled. -->
      <slot></slot>
    </div>
  </template>
  <template v-else>
    <slot></slot>
  </template>
</template>

<style lang="scss" scoped>
.loading-block {
  position: relativ;
}

.spinner-wrapper,
.success-wrapper {
  position: absolute;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: transparentize(#fff, 0.5);
  z-index: 1;
}

.success-wrapper {
  background: #fff;
}
</style>
