<script setup>
import { onMounted, ref } from 'vue'
import Loading from '@/components/Loading.vue'
import Modal from '@/components/Modal.vue'
import CorrectionInput from '@/components/CorrectionInput.vue'
import { useExamStore } from '@/stores/exam'
const examStore = useExamStore()


const showScan = ref(null)

onMounted(examStore.loadList)
</script>
<template>
  <div>
    <div class="mb-3">
      <label class="form-label">Prüfung auswählen</label>
      <select class="form-select" v-model="examStore.selectedExam">
        <option>Mathe 2023</option>
        <option>Französisch 2023</option>
      </select>
    </div>

    <Loading :loading="examStore.list.comp('Loading')">
      <div if="examStore.list.comp('Loaded')">
        <table class="table table-row correction-table">
          <thead>
            <tr>
              <th>Kand. Nr.</th>
              <th>Geb. Dat.</th>
              <th>A1</th>
              <th>A2</th>
              <th>A3</th>
              <th>A4</th>
              <th>Total</th>
              <th>...</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(exam, examIndex) of examStore.list.entries" :class="{ 'invalid': examIndex === 1 }">
              <td>
                1
              </td>
              <td>
                29.01.1997
              </td>
              <td>
                <CorrectionInput :value="5" :accuracy="0.8" />
              </td>
              <td>
                <CorrectionInput :value="5" :accuracy="0.4" />
              </td>
              <td>
                <CorrectionInput :value="8" :accuracy="0.2" />
              </td>
              <td>
                <CorrectionInput :value="5" :accuracy="0.2" />
              </td>
              <td>
                20
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
      <div class="p-3 text-center">
        <button class="btn btn-primary btn-lg">
          <i class="fa-solid fa-file-excel"></i>
          Excel herunterladen
        </button>

      </div>
    </Loading>
    <Modal :show="!!showScan" @close="showScan = false">
      <img src="https://placehold.co/400x800">
    </Modal>
  </div>
</template>
