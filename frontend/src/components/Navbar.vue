<template>
  <div id="nav" class="nav">
    <router-link to="/" class="brand">VIP Retrieval Demo</router-link>

    <nav>
      <router-link :to="{ name: 'about' }" class="nav-item">About</router-link> |
      <router-link :to="{ name: 'upload' }" class="nav-item">Upload</router-link> |
      <router-link :to="{ name: 'webcam' }" class="nav-item">WebCam</router-link>
    </nav>
  </div>
</template>

<script>
export default {
  name: 'Navbar'
}
</script>

<style scoped>

</style>
