import Vue from 'vue'
import VueRouter from 'vue-router'
import ListMovies from '../modules/Movies/views/ListMovies.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'MovieList',
    component: ListMovies
  },
]

const router = new VueRouter({
  mode: 'history',
  routes
})

export default router;