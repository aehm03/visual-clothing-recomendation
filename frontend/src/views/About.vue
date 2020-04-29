<template>
  <div>
  <h1>About</h1>
    <b-card><Info/><VIPLogo class="logo"/></b-card>
  </div>
</template>

<script>
import Info from '../components/Info'
import VIPLogo from '../components/VIPLogo'
export default {
  name: 'About',
  components: {
    Info,
    VIPLogo
  }
}
</script>

<style scoped>
  .logo {
    padding-top: 20rem;
  }

</style>
