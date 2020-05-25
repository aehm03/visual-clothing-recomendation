<template>
  <div>
    <h3>Result:</h3>
    <div >
    <svg width="560" :height="(560*imageDimensions.ratio)" class="flex"
         xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
      <image v-bind:href="this.image_url" width="560"  id="product_image"/>
      <a v-for="(item, index)  in items" :key="index"
        v-b-toggle="'collapse-'+index"
        @click="jumpto(index)">
      <rect
                  v-bind:y="y(item.box[1])"
                  v-bind:x="x(item.box[0])"
                  v-bind:width="(width (item.box[2], item.box[0]))"
                  v-bind:height="(height(item.box[3], item.box[1]))"
                  style="stroke:#00aeef;stroke-width:2;stroke-opacity:0.9;"
                  rx="5" ry="5"
      ><title>{{item.category}}</title></rect></a>
    </svg>
    </div>
    <b-card title="Detected fashion items:" style="max-width: 100%;" id="detected" class="detected">
      <div v-for="(item, index) in items" :key="index"
          class="item"
          v-b-toggle="'collapse-'+index"
      >
        <b-card class="detect-item-card">
        <DetectedImage :image="image_url" :box="item.box" :imageDimensions="imageDimensions" :id="index"/>
        <a>{{item.category}}</a>
        <b-collapse :id="'collapse-'+index" class="mt-2">
            <h5>Matching Products:</h5>
            <b-col>
              <b-row v-if="item.match_products">
                <div v-for="(product, index) in item.match_products" :key="index">
                  <td class="matching-image"><MatchingProduct v-bind:product="product"/></td>
                </div>
              </b-row>
            </b-col>
        </b-collapse>
        </b-card>
      </div>
      <br>
      <b-button block class="mr-3" variant="outline-primary" @click="UploadAnotherPicture">{{ this.buttonMessage }}</b-button>
    </b-card>
    <br>
  </div>
</template>

<script>
import APIService from '../services/APIService'
import MatchingProduct from './MatchingProduct'
import DetectedImage from './DetectedImage'
import Vue from 'vue'

export default {
  name: 'Result',
  components: { MatchingProduct, DetectedImage },
  props: {
    serverResponse: Object,
    imageDimensions: Object,
    buttonMessage: String
  },
  data () {
    return {
      items: [],
      image_url: null
    }
  },

  created: function () {
    this.image_url = process.env.ROOT_API + this.serverResponse.image_url
    this.items = this.serverResponse.items

    this.items.forEach((item) => {
      if (item.category === 'short sleeve top') {
        this.requestMatches(item).then(response => {
          Vue.set(item, 'match_ids', response.data.matches)

          Vue.set(item, 'match_products', [])
          const promises = this.getProducts(item)
          promises.forEach(p => p.then(product => {
            item.match_products.push(product)
          }))
        })
      }
    })
  },
  methods: {
    jumpto (index) {
      window.setTimeout(function () {
        document.getElementById(index).scrollIntoView()
      }, 200)
    },
    getProducts (item) {
      return item.match_ids.map(id => {
        return APIService.getProduct(id).then(response => {
          return response.data
        })
      })
    },
    /* Functions for dimensions of the bounding-boxes, including
    ** rounding of the parameters from the backend that might be
    ** negative or greater one.
     */
    y (fraction) {
      fraction = Math.min(fraction, 1)
      fraction = Math.max(fraction, 0)
      return fraction * 560 * this.imageDimensions.ratio + 1
    },
    x (fraction) {
      fraction = Math.min(fraction, 1)
      fraction = Math.max(fraction, 0)
      return fraction * 560 + 1
    },
    width (fractionOne, fractionTwo) {
      fractionOne = Math.min(fractionOne, 1)
      fractionOne = Math.max(fractionOne, 0)
      fractionTwo = Math.min(fractionTwo, 1)
      fractionTwo = Math.max(fractionTwo, 0)
      return (fractionOne * 560 - fractionTwo * 560) - 1
    },
    height (fractionOne, fractionTwo) {
      fractionOne = Math.min(fractionOne, 1)
      fractionOne = Math.max(fractionOne, 0)
      fractionTwo = Math.min(fractionTwo, 1)
      fractionTwo = Math.max(fractionTwo, 0)
      return (fractionOne * 560 * this.imageDimensions.ratio - fractionTwo * 560 * this.imageDimensions.ratio) - 1
    },
    UploadAnotherPicture () {
      this.$emit('back-to-upload')
    },
    /*
    Requests matches from backend for detected fashion item.
    Sends image, category and box (calculated back to original image size)
    of the product to the backend and saves the response in matching_items
     */
    requestMatches (item) {
      let product = {}
      let url = this.image_url.split('/')
      product.image = url.pop()
      product.category = item.category

      const dimensions = [this.imageDimensions.width, this.imageDimensions.height]
      product.box = item.box.map((el, i) => el * dimensions[i % 2])

      return APIService.match(product)
    }
  }
}
</script>

<style scoped>

</style>
