<template>
  <div class="prodImGrid">
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
      imageUrls: this.product.images.map(i => process.env.ROOT_API + 'api/image/' + i)
    }
  }
}
</script>

<style scoped>

</style>
