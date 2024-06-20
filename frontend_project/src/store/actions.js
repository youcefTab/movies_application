export default {
  setCurrentPage({ commit }, page) {
    commit('SET_CURRENT_PAGE', page)
  },
  setPagination({ commit }, pagination) {
    commit('SET_PAGINATION', pagination)
  },
  setMovies({ commit }, movies) {
    commit('SET_MOVIES', movies)
  }
}