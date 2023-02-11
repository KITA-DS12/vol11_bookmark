<template>
    <v-app>
        <v-card
          height="120"
          color="grey darken-3"
          flat
        >
          <v-card-title class="text-center justify-center py-6">
            <router-link to="/">
              <v-img
                max-height="100"
                max-width="220"
                src="@/assets/shiori-org.png"
                lazy-src="@/assets/lazy-shiori-org.png"
              />
            </router-link>
          </v-card-title>
        </v-card>
        <v-main>
            <router-view />
        </v-main>
    </v-app>
</template>

<script>
export default {
    name: 'App',
}
</script>
