<script setup>
import { onMounted, ref } from 'vue'
import Loading from '@/components/Loading.vue'
import Modal from '@/components/Modal.vue'
import CorrectionInput from '@/components/CorrectionInput.vue'
import ErrorListAlert from '@/components/ErrorListAlert.vue'
import { useExamStore } from '@/stores/exam'
const examStore = useExamStore()

const showExam = ref(null)

const deleteExam = (exam) => {
  if (!confirm("Eintrag wirklich löschen?")) return

  examStore.deleteExam(exam)
}

onMounted(() => {
  examStore.reset()
  examStore.loadLogicalExamList()
})
</script>
<template>
  <div>
    <Loading :loading="examStore.logicalExamList.comp('Loading')">
      <div v-if="examStore.logicalExamList.comp('Loaded')" class="mb-3">
        <label class="form-label">Prüfung auswählen</label>
        <select class="form-select" v-model="examStore.selectedLogicalExam" data-test="logical-exam-select">
          <option :value="null">-- Bitte auswählen --</option>
          <option v-for="(logicalExam, logicalExamIndex) of examStore.logicalExamList.entries" :value="logicalExam"
            :key="logicalExamIndex">
            {{ logicalExam.subject }} {{ logicalExam.year }}
          </option>
        </select>
      </div>
      <div v-if="examStore.logicalExamList.comp('Failed')" class="mb-3">
        <ErrorListAlert :error-list="examStore.logicalExamList.errorMsgList"></ErrorListAlert>
      </div>
    </Loading>

    <Loading :loading="examStore.list.comp('Loading')">
      <div class="table-wrapper" v-if="examStore.list.comp('Loaded')">
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
            <tr v-for="exam of examStore.list.entries"
              :class="{ invalid: exam.score !== examStore.calculateExamScore(exam) }" :key="exam.id" :data-test-id="exam.id">
              <td>
                {{ exam.candidate.number }}
                <br />
                <small>Scan-Datum: {{ $filters.formatDatetime(exam.created_at) }}</small>
              </td>
              <td>
                {{ $filters.formatDate(exam.candidate.date_of_birth) }}
              </td>
              <td v-for="exercise of exam.exercises" :key="exercise.id">
                <CorrectionInput :value="exercise.score" :confidence="exercise.confidence"
                  @change="examStore.updateExerciseScore(exercise.id, $event)" />
              </td>
              <td>
                <CorrectionInput :value="exam.score" :confidence="exam.confidence"
                  @change="examStore.updateExamScore(exam.id, $event)" />
              </td>
              <td>
                <button class="btn btn-secondary" @click="showExam = exam" data-test="show-exam-button">
                  <i class="fa-solid fa-image"></i>
                </button>
                <button class="btn btn-danger" @click="deleteExam(exam)" data-test="delete-exam-button">
                  <i class="fa-solid fa-trash"></i>
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div v-if="examStore.list.comp('Failed')">
        <ErrorListAlert :error-list="examStore.list.errorMsgList"></ErrorListAlert>
      </div>
      <div v-if="examStore.selectedLogicalExam" class="p-3 text-center">
        <template v-if="examStore.exportRequest.comp('Loading')">
          <button class="btn btn-primary btn-lg" type="button" disabled>
            <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
            Excel wird generiert...
          </button>
        </template>
        <template v-else>
          <button class="btn btn-primary btn-lg" @click="examStore.getExport()" type="button">
            <i class="fa-solid fa-file-excel"></i>
            Excel herunterladen
          </button>
        </template>
      </div>
    </Loading>
    <Modal :show="!!showExam" @close="showExam = false">
      <img :src="$filters.imageUrl(showExam.picture_path)" class="w-100" alt="Prüfungsscan" data-test="exam-image"/>
    </Modal>
  </div>
</template>
