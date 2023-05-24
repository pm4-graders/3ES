<script setup>
/**
 * This is a Vue.js component that implements a camera interface for taking photos and uploading them.
 * The component uses the "getUserMedia" method to get access to the camera and display the video feed.
 * It also has a canvas element that is used to take a snapshot of the video feed when the user clicks
 * the "takePhoto" button. The snapshot is then converted to a PNG blob and stored in the "snapshotUrl" variable in the Pinia store.
 */
import { ref, onMounted } from 'vue'
import Modal from '@/components/Modal.vue'
import Loading from '@/components/Loading.vue'
import ErrorListAlert from '@/components/ErrorListAlert.vue'
import { useCameraStore } from '../stores/camera'
import { storeToRefs } from 'pinia'

const cameraRef = ref(null)
const canvasRef = ref(null)

const store = useCameraStore()
const { snapshotUrl, currentRequest } = storeToRefs(store)

const availableDevices = ref([])

/**
 * This is a function that creates a video element
 * and sets the stream from the user's camera as the source of the element.
 */
const createCameraElement = () => {
  const constraints = (window.constraints = {
    audio: false,
    video: {
      facingMode: 'environment',
      width: { ideal: 1800 },
      height: { ideal: 1000 }
    }
  })
  navigator.mediaDevices
    .getUserMedia(constraints)
    .then((stream) => {
      cameraRef.value.srcObject = stream
    })
    .catch((error) => {
      alert(error, "May the browser didn't support or there is some errors.")
    })
}
onMounted(async () => {
  let devices = await navigator.mediaDevices.enumerateDevices()
  devices = devices.filter((device) => device.kind === 'videoinput')
  availableDevices.value = devices
})
onMounted(createCameraElement)
onMounted(() => {
  cameraRef.value.addEventListener('loadedmetadata', (e) => {
    canvasRef.value.width = e.target.videoWidth
    canvasRef.value.height = e.target.videoHeight
  })
})

/**
 * takes a photo and passes the photo to the pinia store
 */
const takePhoto = () => {
  const context = canvasRef.value.getContext('2d')

  context.drawImage(cameraRef.value, 0, 0, canvasRef.value.width, canvasRef.value.height)
  canvasRef.value.toBlob(
    (blob) => {
      store.setSnapshot(blob)
    },
    'image/png',
    1
  )
}

const takePhotoFromGallery = (e) => {
  if (e.currentTarget.files.length === 0) {
  }
  let file = e.currentTarget.files[0]
  store.setSnapshot(file)
  // let reader = new FileReader();
  // reader.addEventListener('load', (fileReadEvent) => {
  //   console.log(fileReadEvent)
  // });
  // reader.readAsText(file);
}

/**
 * resets the current request of taking and sending a photo
 */
const reset = () => {
  store.clearCurrentRequest()
}
</script>
<template>
  <div class="video-container" v-if="currentRequest">
    <div class="device-selector-wrapper">
      <label>Kamera auswählen</label>
      <select class="form-control">
        <option v-for="device of availableDevices">{{ device.label }}</option>
      </select>
    </div>
    <div class="gallery-image-input-wrapper" data-test="photo-from-gallery-button">
      <label class="btn btn-primary d-block" for="galleryImageInput">
        <i class="fa-solid fa-images"></i>
      </label>
      <input
        id="galleryImageInput"
        type="file"
        accept="image/*"
        class="d-none"
        @change="takePhotoFromGallery"
        data-test="photo-from-gallery-input"
      />
    </div>
    <div class="camera-video-wrapper">
      <video class="camera-video" ref="cameraRef" autoplay playsinline muted data-test="camera-video"></video>
    </div>
    <canvas class="canvas-photo" v-show="false" ref="canvasRef"></canvas>

    <div class="actions">
      <button @click="takePhoto" class="btn btn-primary btn-lg" data-test="take-photo-button">
        <i class="fa-solid fa-camera"></i>
      </button>
    </div>
    <Modal :show="!currentRequest.comp('Nil')" @close="reset" data-test="submit-modal">
      <Loading
        :loading="currentRequest.comp('Fetching')"
        :success-badge="currentRequest.comp('Success')"
      >
        <img alt="Dein Scan" :src="snapshotUrl" class="img-fluid w-100 mb-3" data-test="snapshot"/>
        <template v-if="currentRequest.comp('Failed')">
          <ErrorListAlert :error-list="store.currentRequest.errorMsgList"></ErrorListAlert>
          <button @click="reset" class="btn btn-info w-100" data-test="reset-button">
            <i class="fa-solid fa-arrows-rotate"></i>
            Neu aufnehmen
          </button>
        </template>
        <template v-else>
          <button @click="store.uploadResult()" class="btn btn-primary w-100" data-test="submit-button">
            <i class="fa-solid fa-upload"></i>
            Senden
          </button>
        </template>
      </Loading>
    </Modal>
  </div>
</template>
