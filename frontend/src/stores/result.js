import { ref} from 'vue'
import { defineStore } from 'pinia'
import { get } from '@/utilities/fetch'
import { Webresource} from '@/utilities/fetch'
import { requestToWebresource } from '../utilities/fetch'

export const useResultStore = defineStore('result', () => {
  const list = ref(Webresource.Nil)

  const loadList = async () => {
    list.value = Webresource.Loading
    let request = await get('/results')

    list.value = requestToWebresource(request, list.value)
  }

  return { list, loadList }
})
