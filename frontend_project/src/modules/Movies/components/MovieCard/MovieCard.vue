<template>
    <v-card class="py-5 px-5" v-bind="movie">
        <div class="d-flex justify-start align-center">
            <v-img
                max-height="200"
                max-width="200"
                :src="movie.image"
                cover
            ></v-img>
            <div class="mx-10">
                <v-card-tile class="mx-4">{{ movie.title }}</v-card-tile>
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

export default {
    name: 'MovieCard',
    props: {
        movie: {
            type: Object,
            required: true,
        }
    },
    computed: {
        rating: {
            get() {
                console.log(this.movie)
                return this.movie.review && this.movie.review.grade !== undefined ? this.movie.review.grade : 0;
            },
            set(value) {
                // use backend hooks here
                if (!this.movie.review) {
                    this.$set(this.movie, 'review', { grade: value });
                } else {
                    this.$set(this.movie.review, 'grade', value);
                }
            }
        }
    }
}
</script>
