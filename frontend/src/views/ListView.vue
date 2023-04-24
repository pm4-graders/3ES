<script setup>
import { onMounted } from 'vue'
import Loading from '@/components/Loading.vue'
import { useExamStore } from '@/stores/exam'
const examStore = useExamStore()

onMounted(examStore.loadList)
</script>
<template>
  <div>
    <Loading :loading="examStore.list.comp('Loading')">
      <div if="examStore.list.comp('Loaded')">
        {{ examStore.list.entries }}
        <ul class="list-group list-group-stripe">
          <li
            v-for="(entry, index) in examStore.list.entries"
            class="list-group-item"
            :key="entry.id"
            :style="{ transitionDelay: 0.3 * index + 's' }"
          >
            <h4>{{ entry.title }}</h4>
            <div>{{ entry.date }}</div>
          </li>
        </ul>
      </div>
      <div v-if="examStore.list.comp('Failed')">
        <div class="alert alert-danger">{{ examStore.list.request }}</div>
      </div>
    </Loading>
  </div>
</template>
