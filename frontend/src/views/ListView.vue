<script setup>
import { ref, onMounted, computed } from 'vue';
import Modal from '@/components/Modal.vue';
import Loading from '@/components/Loading.vue';
import { useResultStore } from '@/stores/result';
import { Webresource } from '@/utilities/fetch'
const resultStore = useResultStore()

const onEnter = (el, done) => {
  gsap.to(el, {
    opacity: 1,
    height: '1.6em',
    delay: el.dataset.index * 0.15,
    onComplete: done
  })

}

onMounted(resultStore.loadList)
</script>
<template>
  <div>
    <Loading :loading="resultStore.list.comp('Loading')">
      <div if="resultStore.list.comp('Loaded')">
        <TransitionGroup name="list" tag="ul" class="list-group list-group-stripe">
          <li v-for="(entry, index) in resultStore.list.entries" class="list-group-item" :key="entry.id"
            :style="{ transitionDelay: 0.3 * index + 's' }">
            <h4>{{entry.title}}</h4>
            <div>{{ entry.date }}</div>
          </li>
        </TransitionGroup>
      </div>
      <div v-if="resultStore.list.comp('Failed')">
        <div class="alert alert-danger">{{ resultStore.list.request}}</div>
      </div>
    </Loading>
  </div>
</template>
<style scoped>
.list-enter-active,
.list-leave-active {
  transition: all 0.5s ease;
}

.list-enter-from,
.list-leave-to {
  opacity: 0;
  transform: translateX(30px);
}
</style>
