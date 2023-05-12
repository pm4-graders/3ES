<script setup>
/**
 * This component displays a popup dialog window.
 * The component uses Vue3 Transition to animate the modal window when it is shown or hidden. When the modal is shown, it is displayed with an opacity transition and a transform transition to scale it up to its original size. When the modal is hidden, it is hidden with an opacity transition and a transform transition to scale it down to 10% of its original size and to translate it to the top of the screen.
 */
import { defineEmits, defineProps } from 'vue'

/** Emits an event when the user clicks outside of the modal to close it. */
const emit = defineEmits(['close'])

const props = defineProps({
  /** Determines whether the modal is shown or hidden. */
  show: {
    type: Boolean
  },
  /** The title of the modal window. */
  title: {
    type: String
  }
})
</script>
<template>
  <Transition>
    <div v-if="props.show">
      <div class="modal" tabindex="-1" @click="emit('close')">
        <div class="modal-dialog" @click.stop>
          <div class="modal-content">
            <div class="close-btn">
              <button class="btn btn-danger" @click="emit('close')">
                <i class="fa-solid fa-x"></i>
              </button>
            </div>
            <div v-if="props.title" class="modal-header">
              <h5 class="modal-title">{{ props.title }}</h5>
            </div>
            <div class="modal-body">
              <!-- @slot The content of the modal window. -->
              <slot></slot>
            </div>
            <div class="modal-footer" v-if="$slots.footer">
              <!-- @slot The footer content of the modal window. -->
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
    transform: scale(0.5);
  }
}

.v-leave-to {
  opacity: 0;

  .modal-dialog {
    transform: scale(0.1);
    transform: translateY(-100%);
  }
}
</style>
