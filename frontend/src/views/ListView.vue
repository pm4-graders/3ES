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
        <ul class="list-group list-group-stripe">
          <li v-for="(exam, index) in examStore.list.entries" class="list-group-item" :key="exam.id"
            :style="{ transitionDelay: 0.3 * index + 's' }">
            <div class="row">

              <div class="col-9">
                <div>Kandidaten Nr: {{ exam.candidate.number }}</div>
                <div>Geburtstag: {{ $filters.formatDate(exam.candidate.date_of_birth) }}</div>
                <small>Scan-Datum: {{ $filters.formatDatetime(exam.created_at) }}</small>
              </div>
              <div class="col-3">
                <button type="button" class="btn btn-primary">
                  <i class="fa-solid fa-image"></i>
                </button>
              </div>
            </div>
          </li>
        </ul>
      </div>
      <div v-if="examStore.list.comp('Failed')">
        <div class="alert alert-danger">{{ examStore.list.request }}</div>
      </div>
    </Loading>
  </div>
</template>
