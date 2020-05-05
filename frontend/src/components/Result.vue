<template>
  <div>
    <h3>Result:</h3>
    <div class="flex">
    <svg width="560" :height="(560*imageDimensions.ratio)" class="flex"
         xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
      <image v-bind:href="this.image_url" width="560"  id="product_image"/>
      <rect
                  v-for="(item, index)  in items" :key="index"
                  v-bind:y="y(item.box[1])"
                  v-bind:x="x(item.box[0])"
                  v-bind:width="(width (item.box[2], item.box[0]))"
                  v-bind:height="(height(item.box[3], item.box[1]))"
                  style="stroke:#00aeef;stroke-width:2;stroke-opacity:0.9;"
                  v-b-toggle="'collapse-'+index"
                  rx="5" ry="5"
      ><title>{{item.category}}</title></rect>
    </svg>
    </div>
    <b-card title="Detected fashion items:" style="max-width: 100%;">
      <li v-for="(item, index) in items" :key="index"
          class="item"
          v-b-toggle="'collapse-'+index"
      ><a>{{item.category}}</a>
        <b-collapse :id="'collapse-'+index" class="mt-2">
          <b-card title="Matching Products:">
            <b-container>
            <b-col>
              <b-row>
                <div v-if="item.match_products" v-for="product in item.match_products" :key="product">
                  <td class="matching-image"><MatchingProduct v-bind:product="product"/></td>
                </div>
              </b-row>
            </b-col>
            </b-container>
          </b-card>
        </b-collapse>
      </li>
      <br>
      <b-button block class="mr-3" variant="outline-primary" @click="UploadAnotherPicture">{{ this.buttonMessage }}</b-button>
    </b-card>
    <br>
  </div>
</template>

<script>
import APIService from '../services/APIService'
import MatchingProduct from './MatchingProduct'
import Vue from 'vue'

export default {
  name: 'Result',
  components: { MatchingProduct },
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
    this.image_url = 'http://localhost:5000' + this.serverResponse.image_url
    this.items = this.serverResponse.items

    this.items.forEach((item) => {
      this.requestMatches(item).then(response => {
        Vue.set(item, 'match_ids', response.data.matches)

        Vue.set(item, 'match_products', [])
        const promises = this.getProducts(item)
        promises.forEach(p => p.then(product => {
          item.match_products.push(product)
        }))
      })
    })
  },
  methods: {
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
