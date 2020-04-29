<template>
    <div>
<div class="camera">
  <video autoplay class="feed" v-show="!photoTaken" id="camera"></video>
  <div class="gallery" v-show="photoTaken">
  <canvas id="canvas"></canvas>
  </div>
  <br>
  <b-button block class="mr-3" variant="outline-primary" @click="takePicture">{{ this.snapButtonMessage }}</b-button>
  <b-button block @click="upload" class="mr-3" variant="outline-primary" :disabled="!photoTaken">Upload</b-button>
</div>
</div>
</template>

<script>
export default {
  name: 'Camera',
  data () {
    return {
      photo: null,
      photoTaken: false,
      snapButtonMessage: 'SNAP',
      imageDimensions: {
        width: 0,
        height: 0,
        ratio: 0
      },
      videoPlayer: null
    }
  },
  methods: {
    init () {
      if ('mediaDevices' in navigator && 'getUserMedia' in navigator.mediaDevices) {
        navigator.mediaDevices.getUserMedia({video: true}).then(stream => {
          this.videoPlayer = document.querySelector('video')
          this.videoPlayer.srcObject = stream
          this.videoPlayer.play()
        })
      }
    },
    takePicture () {
      if (this.photoTaken) {
        this.photoTaken = false
        this.snapButtonMessage = 'SNAP'
      } else {
        this.snapButtonMessage = 'TAKE ANOTHER PICTURE'
        this.photoTaken = true
        let camera = document.getElementById('camera')
        const picture = document.querySelector('canvas')
        picture.width = camera.clientWidth
        picture.height = camera.clientHeight
        const ctx = picture.getContext('2d')
        ctx.imageSmoothingEnabled = true
        ctx.imageSmoothingQuality = 'high'
        ctx.drawImage(document.querySelector('video'), 0, 0, picture.width, picture.height)
      }
    },
    upload () {
      this.videoPlayer.srcObject.getTracks()[0].stop()
      let canvas = document.getElementById('canvas')
      let dataURL = canvas.toDataURL('image/jpeg', 1.0)
      let blob = this.dataURItoBlob(dataURL)
      let file = new File([blob], 'webCamImage.jpeg', { type: 'image/jpeg' })
      let camera = document.getElementById('canvas')
      this.imageDimensions.width = camera.clientWidth
      this.imageDimensions.height = camera.clientHeight
      this.imageDimensions.ratio = camera.clientHeight / camera.clientWidth
      this.$emit('upload', file, this.imageDimensions)
    },
    dataURItoBlob (dataURI) {
      // convert base64/URLEncoded data component to raw binary data held in a string
      let byteString
      if (dataURI.split(',')[0].indexOf('base64') >= 0) { byteString = atob(dataURI.split(',')[1]) } else { byteString = unescape(dataURI.split(',')[1]) }
      // separate out the mime component
      var mimeString = dataURI.split(',')[0].split(':')[1].split(';')[0]
      // write the bytes of the string to a typed array
      var ia = new Uint8Array(byteString.length)
      for (var i = 0; i < byteString.length; i++) {
        ia[i] = byteString.charCodeAt(i)
      }
      return new Blob([ia], {type: mimeString})
    }
  },
  beforeMount () {
    this.init()
  },
  beforeDestroy () {
    this.videoPlayer.srcObject.getTracks()[0].stop()
  }
}
</script>

<style scoped>
  .camera {
    box-sizing: border-box;
  }

  .feed {
    display: block;
    width: 560px;
    margin: 0 auto;
    background-color: #171717;
    box-shadow: 6px 6px 12px 0 rgba(0, 0, 0, 0.35);
  }

  .gallery {
    box-sizing: border-box;
  }

  canvas {
    display: block;
    width: 560px;
    margin: 0 auto;
    background-color: #171717;
    box-shadow: 6px 6px 12px 0 rgba(0, 0, 0, 0.35);
  }
</style>
