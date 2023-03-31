import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { post, get } from '@/utilities/fetch'
import { Webresource, Request} from '@/utilities/fetch'
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
