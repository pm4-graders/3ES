<script setup>
import { ref, onMounted, computed } from 'vue';
import Modal from '@/components/Modal.vue';
import Loading from '@/components/Loading.vue';
import { useCameraStore } from '../stores/camera';
import { storeToRefs } from 'pinia';
import {Request}from '@/utilities/fetch'


const cameraRef = ref(null);
const canvasRef = ref(null);


const store = useCameraStore();
const {snapshotUrl, currentRequest} = storeToRefs(store)


const createCameraElement = () => {
  const constraints = (window.constraints = {
    audio: false,
    video: true
  })
  navigator.mediaDevices
    .getUserMedia(constraints)
    .then(stream => {
      cameraRef.value.srcObject = stream
    })
    .catch(error => {
      alert(error, "May the browser didn't support or there is some errors.")
    })
}
onMounted(createCameraElement);
onMounted(() => {
  cameraRef.value.addEventListener("loadedmetadata", e => {
    canvasRef.value.width = e.target.videoWidth;
    canvasRef.value.height = e.target.videoHeight;
  })
});

const takePhoto = () => {
  const context = canvasRef.value.getContext('2d')

  context.drawImage(cameraRef.value, 0, 0, canvasRef.value.width, canvasRef.value.height);
  canvasRef.value.toBlob(blob => {
    store.setSnapshot(blob)
  }, 'image/png', 1)

}

const showModal = computed(() => {
  return currentRequest.value.comp('Prepared', 'Failed')
})


const reset = () => {
  store.clearCurrentRequest();
}

</script>
<template>
  <div class="video-container" v-if="currentRequest">
    <div class="camera-video-wrapper">
      <video class="camera-video" ref="cameraRef" autoplay playsinline muted></video>
    </div>
    <canvas class="canvas-photo" v-show="false" ref="canvasRef"></canvas>

    <div class="actions">
      <button @click="takePhoto" class="btn btn-primary btn-lg">
        <i class="fa-solid fa-camera"></i>
      </button>
    </div>
    <Modal :show="!currentRequest.comp('Nil')" @close="reset">
      <Loading :loading="currentRequest.comp('Fetching')"
        :success-badge="currentRequest.comp('Success')">
        <img :src="snapshotUrl" class="img-fluid w-100 mb-3">
        <div class="alert alert-danger" v-if="currentRequest.comp('Failed')">
          {{ store.currentRequest.errorMsg}}</div>
        <button @click="store.uploadResult()" class="btn btn-primary w-100">
          <i class="fa-solid fa-upload"></i>
          Senden</button>
      </Loading>
    </Modal>
  </div>
</template>


