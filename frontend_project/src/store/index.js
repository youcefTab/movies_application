import Vue from 'vue'
import Vuex from 'vuex'
import actions from './actions'
import mutations from './mutations'
import createPersistedState from 'vuex-persistedstate'

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    currentPage: 1,
    pagination: {
      nextPage: null, 
      previousPage: null,
    },
    movies: [],
  },
  mutations,
  actions,
  plugins: [
    createPersistedState({
      key: 'moviesApp',
      paths: ['currentPage', 'pagination', 'movies']
    })
  ],
  modules: {}
})
