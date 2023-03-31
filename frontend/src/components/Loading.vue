<script setup>
const props = defineProps({
  loading: {
    type: Boolean
  },
  successBadge: {

    type: Boolean
  }
})
</script>

<template>
  <template v-if='props.loading || props.successBadge'>
    <div class='loading-block'>
      <div v-if='!props.successBadge' class='spinner-wrapper'>
        <div class='spinner spinner-border text-primary' role='status'>
          <span class='visually-hidden'>Loading...</span>
        </div>
      </div>
      <div v-if='props.successBadge' class='success-wrapper'>
        <i class='fa-solid fa-circle-check fa-3x text-success'></i>
      </div>
      <slot></slot>
    </div>
  </template>
  <template v-else>
    <slot></slot>
  </template>
</template>

<style lang='scss' scoped>
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


.spinner {
}
</style>

