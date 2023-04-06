<script setup>
/**
 * This component renders a list of buttons.
 */

const props = defineProps({
  /**
   *  array of objects, each object representing a button in the list.
   * The object has two properties: title and path, which represent the button's text
   * and the URL that the button should link to, respectively.
   */
  list: {
    required: true,
    type: Array
  }
})
</script>

<template>
  <div class="button-container text-center">
    <div class="button-group">
      <div v-for="entry of props.list" class="col p-3 border bg-light">
        <a :href="entry.path">{{ entry.title }}</a>
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
