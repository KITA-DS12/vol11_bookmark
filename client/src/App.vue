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
                max-height="150"
                max-width="290"
                src="@/assets/logo.png"
                style="margin-top: -10px"
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
