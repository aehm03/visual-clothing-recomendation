<template>
  <div>
    <h3>Product</h3>
    <img v-for="imageUrl in imageUrls" :key="imageUrl" class="prodImage" :src="imageUrl"/>
  </div>
</template>

<script>

export default {
  name: 'MatchingProduct',
  props: {
    product: Object
  },
  data () {
    return {
      imageUrls: this.product.images.map(i => 'http://localhost:5000/api/image/' + i)
    }
  }
}
</script>

<style scoped>

</style>
