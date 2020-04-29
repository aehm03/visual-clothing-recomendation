import Vue from 'vue'
import VueRouter from 'vue-router'
import About from '../views/About'
import Upload from '../views/Upload'
import NotFound from '../views/NotFound'
import WebCam from '../views/WebCam'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'about',
    component: About
  },
  {
    path: '/upload',
    name: 'upload',
    component: Upload,
    props: true
  },
  {
    path: '/webcam',
    name: 'webcam',
    component: WebCam,
    props: true
  },
  {
    path: '*',
    name: 'notfound',
    component: NotFound,
    props: true
  }
]

const router = new VueRouter({
  mode: 'history',
  routes
})

export default router
