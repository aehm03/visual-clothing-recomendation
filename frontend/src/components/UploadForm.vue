<template>
<b-card>
    <b-container class="bv-example-row" fluid="true">
      <b-row>
        <b-col class="box">
          <div class="spin-container" v-show="loading">
            <atom-spinner
            :animation-duration="1000"
            :size="60"
            color="#00aeef"
            class="spinner"
            />
          </div>
          <p>Upload a picture to detect fashion-items!</p>
          <b-form-file
            accept="image/*"
            v-model="file"
            :state="null"
            placeholder="Choose a file or drop it here..."
            drop-placeholder="Drop file here..."
    ></b-form-file>
          <b-alert
            :show="forbiddenFormat"
            variant="warning"
            id="formatWarning">Wrong file format.</b-alert>
    <b-button
      block
      @click="submit"
      class="mr-3"
      :disabled="file === null"
      variant="outline-primary">Submit</b-button>
    </b-col>
      </b-row>
    </b-container>
</b-card>
</template>

<script>
import { AtomSpinner } from 'epic-spinners'
export default {
  name: 'UploadForm',
  components: {AtomSpinner},
  data () {
    return {
      file: null,
      imageDimensions: {
        width: 0,
        height: 0,
        ratio: 0
      },
      forbiddenFormat: false,
      loading: false
    }
  },
  watch: {
    file (newFile) {
      if (newFile && !newFile.type.startsWith('image/')) {
        this.$nextTick(() => {
          this.file = null
          this.forbiddenFormat = true
        })
      }
      if (newFile && newFile.type.startsWith('image/')) {
        this.forbiddenFormat = false
      }
    }
  },
  methods: {
    submit () {
      this.loading = true
      let reader = new FileReader()
      reader.readAsDataURL(this.file)
      reader.onload = evt => {
        let img = new Image()
        img.onload = () => {
          this.imageDimensions.width = img.width
          this.imageDimensions.height = img.height
          this.imageDimensions.ratio = img.height / img.width
        }
        img.src = evt.target.result
      }
      this.$emit('submit', this.file, this.imageDimensions)
    }
  }
}
</script>

<style scoped>

</style>
