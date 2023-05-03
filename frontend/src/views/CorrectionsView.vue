<script setup>
import { onMounted, ref } from 'vue'
import Loading from '@/components/Loading.vue'
import Modal from '@/components/Modal.vue'
import CorrectionInput from '@/components/CorrectionInput.vue'
import { useExamStore } from '@/stores/exam'
const examStore = useExamStore()

const showScan = ref(null)

onMounted(examStore.loadLogicalExamList)
</script>
<template>
  <div>
    <Loading :loading="examStore.logicalExamList.comp('Loading')">
      <div v-if="examStore.logicalExamList.comp('Loaded')" class="mb-3">
        <label class="form-label">Prüfung auswählen</label>
        <select class="form-select" v-model="examStore.selectedLogicalExam">
          <option :value="null">-- Bitte auswählen --</option>
          <option
            v-for="(logicalExam, logicalExamIndex) of examStore.logicalExamList.entries"
            :value="logicalExam"
            :key="logicalExamIndex"
          >
            {{ logicalExam.subject }} {{ logicalExam.year }}
          </option>
        </select>
      </div>
    </Loading>

    <Loading :loading="examStore.list.comp('Loading')">
      <div v-if="examStore.list.comp('Loaded')">
        <table class="table table-row correction-table">
          <thead>
            <tr>
              <th>Kand. Nr.</th>
              <th>Geb. Dat.</th>
              <th v-for="exercise of examStore.list.entries[0].exercises" :key="exercise.id">
                {{ exercise.number }}
              </th>
              <th>Total</th>
              <th>...</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="exam of examStore.list.entries"
              :class="{ invalid: exam.score !== examStore.calculateExamScore(exam) }"
              :key="exam.id"
            >
              <td>
                {{ exam.candidate.number }}
                <br>
                <small>Scan-Datum: {{$filters.formatDatetime(exam.created_at)}}</small>
              </td>
              <td>
                {{ $filters.formatDate(exam.candidate.date_of_birth) }}
              </td>
              <td v-for="exercise of exam.exercises" :key="exercise.id">
                <CorrectionInput
                  :value="exercise.score"
                  :confidence="exercise.confidence"
                  @change="examStore.updateExerciseScore(exercise.id, $event)"
                />
              </td>
              <td>
                <CorrectionInput
                  :value="exam.score"
                  :confidence="exam.confidence"
                  @change="examStore.updateExamScore(exam.id, $event)"
                />
              </td>
              <td>
                <button class="btn btn-secondary" @click="showScan = true">scan</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div v-if="examStore.list.comp('Failed')">
        <div class="alert alert-danger">{{ examStore.list.request }}</div>
      </div>
      <div v-if="examStore.selectedLogicalExam" class="p-3 text-center">
        <button class="btn btn-primary btn-lg">
          <i class="fa-solid fa-file-excel"></i>
          Excel herunterladen
        </button>
      </div>
    </Loading>
    <Modal :show="!!showScan" @close="showScan = false">
      <img src="https://placehold.co/400x800" />
    </Modal>
  </div>
</template>
