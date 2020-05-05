<template>
  <div id="app">
    <Navbar/>
    <router-view/>
  </div>
</template>

<script>
import Navbar from './components/Navbar'
export default {
  name: 'App',
  components: {Navbar},
  data () {
    return {
      upload: false
    }
  }
}
</script>

<style>
  @import '/assets/style.css';
</style>
