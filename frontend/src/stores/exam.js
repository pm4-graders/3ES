import { ref, watch } from 'vue'
import { defineStore } from 'pinia'
import { get, Webresource, Request, post, deleteReq } from '@/utilities/fetch'
import { requestToWebresource } from '../utilities/fetch'
import download from '@/utilities/download'
import filters from '@/utilities/filters'

export const useExamStore = defineStore('exam', () => {
  const list = ref(Webresource.Nil)

  const selectedLogicalExam = ref(null)

  const logicalExamList = ref(Webresource.Nil)
  const exportRequest = ref(Request.Nil)

  const reset = () => {
    selectedLogicalExam.value = null
    logicalExamList.value = Webresource.Nil
    list.value = Webresource.Nil
  }

  const loadList = async () => {
    list.value = Webresource.Loading

    let reqUrl = '/exams'
    if (selectedLogicalExam.value) {
      let { year, subject } = selectedLogicalExam.value
      reqUrl += `?year=${year}&subject=${subject}`
    }
    let request = await get(reqUrl, null, {}, 'exams')

    list.value = requestToWebresource(request, list.value)
  }
  const loadLogicalExamList = async () => {
    logicalExamList.value = Webresource.Loading
    let request = await get('/logical-exams', null, {}, 'logical_exams')

    logicalExamList.value = requestToWebresource(request, list.value)
  }

  const updateExerciseScore = async (exerciseId, score) => {
    let request = {
      value: Request.PreparedOf({ params: { score } })
    }
    await post(`/exercises/${exerciseId}`, request)
    loadList()
  }
  const updateExamScore = async (examId, score) => {
    let request = {
      value: Request.PreparedOf({ params: { score } })
    }
    await post(`/exams/${examId}`, request)
    loadList()
  }

  const calculateExamScore = (exam) => {
    return exam.exercises.reduce((total, exercise) => exercise.score + total, 0)
  }

  const deleteExam = async (exam) => {
    await deleteReq(`/exams/${exam.id}`)
    await loadList()
  }

  const getExport = async () => {
    let reqUrl = '/logical-exams/export'
    if (selectedLogicalExam.value) {
      let { year, subject } = selectedLogicalExam.value
      reqUrl += `?year=${year}&subject=${subject}`
    }
    let request = await get(reqUrl, exportRequest, {}, 'path')
    download(filters.imageUrl(request.data), request.data.split('/').reverse()[0])
  }

  watch(selectedLogicalExam, () => {
    loadList()
  })

  return {
    list,
    loadList,
    logicalExamList,
    loadLogicalExamList,
    selectedLogicalExam,
    updateExerciseScore,
    updateExamScore,
    calculateExamScore,
    reset,
    deleteExam,
    getExport,
    exportRequest
  }
})
