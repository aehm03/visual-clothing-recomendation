<template>
    <div>
      <b-img :src="logo_url" fluid-grow/>
    </div>
</template>

<script>
export default {
  name: 'VIPLogo',
  data () {
    return {
      logo_url: '../static/vip-logo-large.png'
    }
  }
}
</script>

<style scoped>

</style>
