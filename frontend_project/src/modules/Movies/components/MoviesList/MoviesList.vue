<template>
    <div>
        <div class="d-flex justify-center align-center mt-3 mb-3">
            <div class="text-h5">
                La Liste de vos films préférés 
            </div>
        </div>
        <v-data-iterator :items-per-page="5" :page="currentPage" :items="movies" @update:page="updatePage" hide-default-footer>
            <template v-slot:default="{ items }">
                <div
                    :key="item.id"
                    v-for="(item) in items"
                    class="px-5 py-3 d-flex justify-center align-center flex-column"
                >
                    <MovieCard :movie="{...item, image: `https://picsum.photos/200?random=${item.id}`}" />
                </div>
            </template>
        </v-data-iterator>
        <div v-if="pagination.nextPage || pagination.previousPage" class="pagination">
            <v-btn class="ma-2" @click="goToPage(pagination.previousPage)" :disabled="!pagination.previousPage">
                <v-icon
                    icon="mdi-arrow-left"
                    start
                ></v-icon>
                    Previous
            </v-btn>
            <v-btn class="ma-2" @click="goToPage(pagination.nextPage)" :disabled="!pagination.nextPage">
                Next
            </v-btn>
        </div>
    </div>
</template>

<script>

import MovieCard from '../MovieCard/MovieCard.vue'
import { mapState, mapActions } from 'vuex'
import api from '../../../../utils/axios'

export default {
    name: 'MoviesList',
    components: {
        MovieCard,
    },
    computed: {
        ...mapState(['currentPage', 'pagination', 'movies'])
    },
    methods: {
        ...mapActions(['setCurrentPage', 'setPagination', 'setMovies']),
        updatePage(page) {
            this.setCurrentPage(page)
        },
        async getMovies(url = '/movies-app/movies/') {
            try {
                const response = await api.get(url, {
                    params: {
                        page_size: 5
                    }
                })
                this.setMovies(response.data.results)
                this.setPagination({
                    nextPage: response.data.next,
                    previousPage: response.data.previous
                })
            } catch (error) {
                console.error('Error fetching movies:', error)
            }
        },
        goToPage(url) {
            if (url) {
                this.getMovies(url)
            }
        }
    },
    created() {
        if (!this.movies.length) this.getMovies()
    }
}
</script>

<style scoped>
.pagination {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-top: 20px;
}
</style>