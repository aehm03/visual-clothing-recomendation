<template>
<div>
  <div class="crop-container" :style="'height:'+cropHeight+'px;width:100px;'">
    <img :src="image"
         id="detectedImage"
         class="detected-image"
         :style="'width:'+imageWidth+'px;margin:'+imageMarginTop+'px 0px 0px '+imageMarginLeft+'px;'"
    >
  </div>
</div>
</template>

<script>
export default {
  name: 'DetectedImage',
  props: {
    image: String,
    box: Array,
    imageDimensions: Object
  },
  data () {
    return {
      imageWidth: 0,
      cropHeight: 0,
      imageMarginTop: 0,
      imageMarginLeft: 0
    }
  },
  mounted () {
    let boxHeight = this.box[3] - this.box[1]
    let boxWidth = this.box[2] - this.box[0]
    this.imageWidth = 100 / boxWidth
    let boxRatio = (boxWidth * this.imageDimensions.width) / (boxHeight * this.imageDimensions.height)
    this.cropHeight = 100 / boxRatio
    this.imageMarginTop = this.box[1] * ((100 / boxWidth) * this.imageDimensions.ratio) * (-1)
    this.imageMarginLeft = this.box[0] * (100 / boxWidth) * (-1)
  }
}
</script>

<style scoped>

</style>
