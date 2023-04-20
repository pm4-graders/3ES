import { ref } from 'vue'
import { defineStore } from 'pinia'
import { get, Webresource } from '@/utilities/fetch'
import { requestToWebresource } from '../utilities/fetch'

export const useExamStore = defineStore('exam', () => {
  const list = ref(Webresource.Nil)

  const selectedExam = ref('')

  const loadList = async () => {
    list.value = Webresource.Loading
    let request = await get('/exams')

    list.value = requestToWebresource(request, list.value)
  }


  return { list, loadList, selectedExam }
})
