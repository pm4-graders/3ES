<script setup>
import { defineEmits, defineProps, computed } from 'vue'

const emit = defineEmits(['close'])

const props = defineProps({
  show: {
    type: Boolean,
  },
  title: {
    type: String,
  }
});


const style = computed(() => {
  return {
    'display': 'block'
  }
});


</script>
<template>
  <Transition>
    <div v-if="props.show">
      <div class="modal" tabindex="-1" @click="emit('close')">
        <div class="modal-dialog" @click.stop>
          <div class="modal-content">
            <div v-if="props.title" class="modal-header">
              <h5 class="modal-title">{{ props.title }}</h5>
            </div>
            <div class="modal-body">
              <slot></slot>
            </div>
            <div class="modal-footer" v-if="$slots.footer">
              <slot name="footer"></slot>
            </div>
          </div>
        </div>
      </div>
    </div>
  </Transition>
</template>

<style lang="scss" scoped>

.v-enter-active {
  transition: opacity 0.5s ease;

  .modal-dialog {
    transition: transform 0.2s ease;
  }
}

.v-leave-active {
  transition: opacity 0.5s ease;
  .modal-dialog {
    transition: transform 0.8s ease;
  }
}

.v-enter-from {
  opacity: 0;

  .modal-dialog {
    transform: scale(.5);
  }
}

.v-leave-to {
  opacity: 0;

  .modal-dialog {
    transform: scale(.1);
    transform: translateY(-100%);
  }
}</style>

