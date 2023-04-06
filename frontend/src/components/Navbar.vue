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
  <nav class="navbar navbar-expand navbar-dark bg-dark fixed-bottom">
    <div class="container-fluid justify-content-center nav navbar-nav">
      <div v-for="entry of props.list" class="nav-item">
        <router-link class="nav-link m-2 p-3" :to="entry.path">
          <a>{{ entry.title }}</a>
        </router-link>
      </div>
    </div>
  </nav>

</template>

<style lang="scss" scoped>

.nav-item {
  max-width: 250px;
  min-width: 100px;
  width: 20%;
  margin: 0 5px;
}
.nav-link {
  width: 100%;
  text-align: center;
  border-radius: 5px;
  background-color: #304FCC;
  color: #ffffff;
}

</style>
