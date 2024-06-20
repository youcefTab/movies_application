<template>
    <v-card class="py-5 px-5" v-bind="movie" max-width="700">
        <div class="d-flex justify-start align-center">
            <v-img
                max-height="200"
                max-width="200"
                :src="movie.image"
                cover
            ></v-img>
            <div class="mx-10" max-width="400">
                <v-card-title :name="movie.title" class="mx-4">{{ movie.title }}</v-card-title>
                <v-card-text>Résumé : {{ movie.description }}</v-card-text>
                <div class="text-center">
                    <v-rating
                    v-model="rating"
                    hover
                    ></v-rating>
                </div>
            </div>
        </div>
    </v-card>
</template>

<script>
import { mapActions, mapState } from 'vuex'
import api from '../../../../utils/axios'

export default {
    name: 'MovieCard',
    props: {
        movie: {
            type: Object,
            required: true,
        }
    },
    methods: {
        ...mapActions(['setMovies']),
    },
    computed: {
        ...mapState(['movies']),
        rating: {
            get() {
                return this.movie.review && this.movie.review.grade !== undefined ? this.movie.review.grade : 0
            },
            async set(value) {
                let response 
                try {
                    if (!this.movie.review) {
                        response = await api.post('/movies-app/reviews/', { movieId: this.movie.id, grade: value })
                    } else {
                        response = await api.put(`/movies-app/reviews/${this.movie.review.id}/`, { movieId: this.movie.id, grade: value })
                    }
                } catch (error) {
                    console.log("Error when trying to add your review")
                }
                
                this.setMovies(this.movies.map((movie) => movie.id == this.movie.id ? { ... this.movie, review: response.data } : movie))
            }
        }
    }
}
</script>
