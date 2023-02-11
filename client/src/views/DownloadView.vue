<template>
<v-app>
<v-list color="blue-grey lighten-5" style="height: 42vh; overflow-y: auto;">
    <v-list-item-group v-model="selectedUser" color="primary">
        <v-list-item v-for="user in users" :key="user" @click="selectUser">
        <v-sheet
        color="grey-lighten-4"
        class="pa-4"
      　>
        <v-avatar
          class="mb-4"
          color="grey-darken-1"
          size="32"
        ></v-avatar>

        <div><v-icon>mdi-folder</v-icon></div>
      </v-sheet>
            <v-list-item-icon>
                <v-icon>1</v-icon>
            </v-list-item-icon>
            <v-list-item-icon>
                <v-icon>2</v-icon>
            </v-list-item-icon>
            <v-list-item-icon>
                <v-icon></v-icon>
            </v-list-item-icon>

            <v-list-item-content>
                <v-list-item-title>{{ user }}</v-list-item-title>
            </v-list-item-content>
        </v-list-item>
    </v-list-item-group>
</v-list>
<v-btn
      class="mx-2"
      fab
      dark
      large
      color="green"
    >
    <v-icon dark>
        mdi-upload
      </v-icon>
    </v-btn>
    <v-btn
      class="mx-2"
      fab
      dark
      large
      color="purple"
    >
      <v-icon dark>
        mdi-download
      </v-icon>
    </v-btn>
</v-app>
</template>

<script>
    export default {
    data () {
      return {
        users: [
          "user1",
          "user2",
          "user3",
          "user1",
          "user2",
          "user3",
          "user1",
          "user2",
          "user3",
        ]
      }
  }
}
</script>


