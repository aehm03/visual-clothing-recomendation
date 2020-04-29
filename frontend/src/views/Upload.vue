<template>
  <div>
  <h1>Upload</h1>
  <UploadForm v-if="!upload_success" @submit="Submit"/>
      <Result v-if="upload_success" v-bind:server-response="this.serverResponse"
              :button-message="'Upload another picture!'"
          v-bind:imageDimensions="this.imageDimensions" @back-to-upload="Back"/>
  </div>
</template>

<script>
import UploadForm from '../components/UploadForm'
import Result from '../components/Result'
import APIService from '../services/APIService'
export default {
  name: 'Upload',
  components: {Result, UploadForm},
  data () {
    return {
      file: null,
      upload_success: false,
      serverResponse: null,
      imageDimensions: {}
    }
  },
  methods: {
    Submit (file, image) {
      this.imageDimensions = image
      this.file = file
      let formData = new FormData()
      formData.append('file', this.file)
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
  .flex {
    display: flex;
    justify-content: center;
    align-items: center;
    vertical-align: middle;
}
</style>
