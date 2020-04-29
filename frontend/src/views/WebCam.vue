<template>
<div>
<h1>WebCam</h1>
<Camera @upload="Upload" v-if="!upload_success"/>
<Result v-if="upload_success" v-bind:server-response="this.serverResponse"
        :button-message="'Take another picture!'"
          v-bind:imageDimensions="this.imageDimensions" @back-to-upload="Back"/>
</div>
</template>

<script>
import Camera from '../components/Camera'
import APIService from '../services/APIService'
import Result from '../components/Result'
export default {
  name: 'WebCam',
  components: { Camera, Result },
  data () {
    return {
      imageDimensions: {},
      upload_success: false,
      serverResponse: null,
      file: null
    }
  },
  methods: {
    Upload (file, imageDimensions) {
      this.imageDimensions = imageDimensions
      let formData = new FormData()
      formData.append('file', file)
      APIService.detect(formData)
        .then(response => {
          this.serverResponse = response.data
          this.upload_success = true
        })
        .catch(error => {
          console.log('These errors occured: ' + error.response)
        })
    },
    Back () {
      this.upload_success = false
    }
  }
}
</script>

<style scoped>

</style>
