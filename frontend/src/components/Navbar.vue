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
      <div v-for="(entry, entryIndex) of props.list" class="nav-item" :key="entryIndex" >
        <router-link class="nav-link m-2 p-3" active-class="app-nav-active" :to="entry.path">
          <a>{{ entry.title }}</a>
        </router-link>
      </div>
    </div>
  </nav>
</template>

<style lang="scss" scoped>
.nav-item {
  width: 200px;
  margin: 0 5px;
}

.nav-link {
  width: 100%;
  text-align: center;
  border-radius: 5px;
  background-color: #304fcc;
  color: #ffffff;
}

.app-nav-active {
  background-color: #001561;
  color: #ffffff;
}
</style>
