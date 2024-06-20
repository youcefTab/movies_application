<template>
    <div>
        <div class="d-flex justify-center align-center mt-3 mb-3">
            <div class="text-h5">
                La Liste de vos films préférés 
            </div>
        </div>
        <v-data-iterator :items-per-page="5" :page="currentPage" :items="movies" @update:page="updatePage">
            <template v-slot:default="{ items }">
                <div
                    :key="item.id"
                    v-for="(item) in items"
                    class="px-5 py-3"
                >
                    <MovieCard :movie="{...item, image: `https://picsum.photos/200?random=${item.id}`}" />
                </div>
            </template>
        </v-data-iterator>
    </div>
</template>

<script>

import MovieCard from '../MovieCard/MovieCard.vue'
import { mapState, mapActions } from 'vuex'

export default {
    name: 'MoviesList',
    components: {
        MovieCard,
    },
    computed: {
        ...mapState(['currentPage'])
    },
    methods: {
        ...mapActions(['setCurrentPage']),
        updatePage(page) {
            this.setCurrentPage(page)
        }
    },
    data() {
        return {
            movies: [
                {
                    id: 1,
                    title: 'Star wars 1',
                    description: 'The worst movie ever',
                    review: {
                        grade: 3,
                    }
                }, 
                {
                    id: 2, 
                    title: 'Spider Man 2',
                    description: 'The best Movie ever',
                },
                {
                    id: 3,
                    title: 'Star wars 3',
                    description: 'The worst movie ever',
                }, 
                {
                    id: 4, 
                    title: 'Spider Man 4',
                    description: 'The best Movie ever',
                },
                {
                    id: 5,
                    title: 'Star wars 5',
                    description: 'The worst movie ever',
                }, 
                {
                    id: 6, 
                    title: 'Spider Man 6',
                    description: 'The best Movie ever',
                },
                {
                    id: 7,
                    title: 'Star wars 7',
                    description: 'The worst movie ever',
                }, 
                {
                    id: 8, 
                    title: 'Spider Man 8',
                    description: 'The best Movie ever',
                },
                {
                    id: 9,
                    title: 'Star wars 9',
                    description: 'The worst movie ever',
                }, 
                {
                    id: 10, 
                    title: 'Spider Man 10',
                    description: 'The best Movie ever',
                },
                {
                    id: 11,
                    title: 'Star wars 11',
                    description: 'The worst movie ever',
                }, 
                {
                    id: 12, 
                    title: 'Spider Man 12',
                    description: 'The best Movie ever',
                },
                {
                    id: 13,
                    title: 'Star wars 13',
                    description: 'The worst movie ever',
                }, 
                {
                    id: 14, 
                    title: 'Spider Man 14',
                    description: 'The best Movie ever',
                },
                {
                    id: 15,
                    title: 'Star wars 15',
                    description: 'The worst movie ever',
                }, 
                {
                    id: 16, 
                    title: 'Spider Man 16',
                    description: 'The best Movie ever',
                },
                {
                    id: 17,
                    title: 'Star wars 17',
                    description: 'The worst movie ever',
                }, 
                {
                    id: 18, 
                    title: 'Spider Man 18',
                    description: 'The best Movie ever',
                },
                {
                    id: 19,
                    title: 'Star wars 19',
                    description: 'The worst movie ever',
                }, 
                {
                    id: 20, 
                    title: 'Spider Man 20',
                    description: 'The best Movie ever',
                },
                {
                    id: 21,
                    title: 'Star wars 21',
                    description: 'The worst movie ever',
                }, 
                {
                    id: 22, 
                    title: 'Spider Man 22',
                    description: 'The best Movie ever',
                }
            ]
        }

    }
}
</script>