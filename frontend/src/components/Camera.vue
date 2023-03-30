<script setup>
import { ref, onMounted, computed } from 'vue';


const isPhotoTaken = ref(false);
const cameraRef = ref(null);
const cameraWrapperRef= ref(null);
const canvasRef = ref(null);


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

const takePhoto = () => {
  const context = canvasRef.value.getContext('2d')
  context.imageSmoothingEnabled = true

  context.drawImage(cameraRef.value, 0, 0, canvasRef.value.width, canvasRef.value.height);
  isPhotoTaken.value = true;

}

const canvasStyle = () => {
  if(!cameraRef.value) {
    return {};
  }
  const rect = cameraRef.value.getBoundingClientRect()
  return {
    width: `${rect.width}px`,
    height: `${rect.height}px`,
  }
}

</script>
<template>
  <div class="video-container">
    <div class="camera-video-wrapper" ref="cameraWrapperRef">
      <video class="camera-video" ref="cameraRef" autoplay playsinline ></video>
    </div>
    <canvas v-show="isPhotoTaken" :style="canvasStyle()" class="canvas-photo" ref="canvasRef"></canvas>

    <div class="actions">
      <button @click="takePhoto" class="btn btn-primary">Snap!</button>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.video-container {
  position: relative;
  display: flex;
    justify-content: center;
    

  .camera-video {
    max-width: 100%;
    width: 800px;
    height: auto;
  }

  .canvas-photo {
    position: absolute;
    left: 0;
    top: 0;

  }

  >.actions {
    position: absolute;
    display: flex;
    justify-content: center;
    left: 0;
    bottom: 0;
    padding: 1rem;
    width: 100%;
  }
}
</style>

