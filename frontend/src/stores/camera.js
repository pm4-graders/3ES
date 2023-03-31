import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { post, Request } from '@/utilities/fetch'

export const useCameraStore = defineStore('camera', () => {
  let currentRequest = ref(Request.Nil)
  const blob = ref(null)

  function setSnapshot(snapshotBlob) {
    currentRequest.value = Request.PreparedOf({ params: { blob: snapshotBlob } })
    blob.value = snapshotBlob
  }

  const snapshotUrl = computed(() => {
    if (blob.value) {
      return URL.createObjectURL(blob.value)
    }
    return null;
  })

  async function uploadResult() {
    currentRequest.value = await post('/upload', currentRequest)

    if (currentRequest.value.comp('Success')) {
      setTimeout(clearCurrentRequest, 2000)
    }
  }

  function clearCurrentRequest() {
    currentRequest.value = Request.Nil
  }

  return {
    uploadResult,
    currentRequest,
    setSnapshot,
    clearCurrentRequest,
    snapshotUrl,
   blob 
  }
})
