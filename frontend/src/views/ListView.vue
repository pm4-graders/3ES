<script setup>
import {  onMounted} from 'vue';
import Loading from '@/components/Loading.vue';
import { useResultStore } from '@/stores/result';
const resultStore = useResultStore()

onMounted(resultStore.loadList)
</script>
<template>
  <div>
    <Loading :loading="resultStore.list.comp('Loading')">
      <div if="resultStore.list.comp('Loaded')">
        <ul class="list-group list-group-stripe">
          <li v-for="(entry, index) in resultStore.list.entries" class="list-group-item" :key="entry.id"
            :style="{ transitionDelay: 0.3 * index + 's' }">
            <h4>{{entry.title}}</h4>
            <div>{{ entry.date }}</div>
          </li>
        </ul>
      </div>
      <div v-if="resultStore.list.comp('Failed')">
        <div class="alert alert-danger">{{ resultStore.list.request}}</div>
      </div>
    </Loading>
  </div>
</template>