<template>
  <v-app>
    <Header />
    <v-main>
      <v-container>
        <router-view/>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
import Header from './modules/Layout/Header/Header'

export default {
  name: 'App',
  components: {
    Header,
  }

  // data: () => ({
  //   //
  // }),
};
</script>
