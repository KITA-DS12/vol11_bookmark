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
  </v-app>
</template>

<script>
import axios from "axios";

export default {
    name: 'Home',
    data () {
      return {
        content: ''
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
            console.log(res)
          })
          .catch((err) => {
            console.log(err);
          });
      }
    }
  }
</script>
