<template>
  <v-app>
    <v-row justify="center" style="text-align: center" align-content="center">
      <v-col cols=3>
        <v-file-input
          accept=".html"
          label="File input"
          outlined
          dense
          @change="getFileContent"
        />
      </v-col>
      <v-col cols=3>
        <v-btn
          fab
          dark
          color="indigo"
          @click="uploadFile"
        >
        <v-icon dark>
          mdi-upload
        </v-icon>
        </v-btn>
      </v-col>
      <v-col cols=3>
        <v-btn
          fab
          dark
          color="indigo"
        >
        <v-icon dark>
          mdi-download
        </v-icon>
        </v-btn>
      </v-col>
    </v-row>
    <v-card
      color="grey-lighten-4"
      class="pa-4"
      v-for="folder in response_children" :key="folder"
    >
      {{ folder.title }}
      <v-list color="blue-grey lighten-5" style="height: 42vh; overflow-y: auto;">
        <v-list-item-group color="primary">
         <v-list-item v-for="data in folder.children" :key="data">
            <v-list-item-icon>
              <v-icon>mdi-account</v-icon>
            </v-list-item-icon>
            <v-list-item-content>
              <v-list-item-title>{{ data.title }}</v-list-item-title>
              <v-list-item-title>{{ data.url }}</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </v-list-item-group>
      </v-list>
    </v-card>
  </v-app>
</template>

<script>
import axios from "axios";

export default {
    name: 'Home',
    data () {
      return {
        content: '',
        response_json: null,
        response_children: null
      }
    },
    methods: {
      async getFileContent(file) {
        try {
          const content = await this.readFileAsync(file)
          this.content = content
        } catch (e) {
          console.log(e)
        }
      },
      readFileAsync(file) {
        return new Promise((resolve, reject) => {
          const reader = new FileReader()
          reader.onload = () => {
            resolve(reader.result)
          }
          reader.onerror = reject
          reader.readAsDataURL(file)
        })
      },
      async uploadFile() {
        console.log(this.content)
        await axios
          .post("html-json", {
            bookmark: this.content.slice(22)
          })
          .then((res) => {
            this.response_json = res.data
            this.response_children = this.response_json.children
            for ( const data in this.response_children) {
              console.log(this.response_children[data].children)
            }
          })
          .catch((err) => {
            console.log(err);
          });
      }
    }
  }
</script>
