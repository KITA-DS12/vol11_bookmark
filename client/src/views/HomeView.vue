<template>
  <v-app>
    <v-row justify="center" style="text-align: center" align-content="center">
      <v-col cols=3>
        <v-file-input
          accept=".html"
          label="File input"
          chips
          @change="getFileContent"
        />
      </v-col>
      <v-col cols=2>
        <v-btn
          fab
          dark color="indigo"
          @click="uploadFile"
        >
        <v-icon dark>
          mdi-upload
        </v-icon>
        </v-btn>
      </v-col>
      <v-col cols=2>
        <v-btn
          fab
          dark
          color="indigo"
          @click="reloadFile"
        >
        <v-icon dark>
          mdi-reload
        </v-icon>
        </v-btn>
      </v-col>
      <v-col cols=2>
        <v-btn
          fab
          dark
          color="indigo"
          @click="downloadFile"
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
      v-for="folder in response_children"
    >
      {{ folder.title }}
      <v-list color="blue-grey lighten-5" style="height: 30vh; overflow-y: auto;">
       <v-list-item v-for="data in folder.children">
          <v-list-item-avatar>
            <img :src="data.icon">
          </v-list-item-avatar>
          <v-list-item-content>
            <v-text-field
              v-model="data.title"
              filled
              label="title"
              clearable
            ></v-text-field>
            <v-list-item-title><a :href="data.url">{{ data.url }}</a></v-list-item-title>
          </v-list-item-content>
        </v-list-item>
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
        response_bookmarkbar: null,
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
          .post("upload", {
            bookmark: this.content.slice(22)
          })
          .then((res) => {
            this.response_json = res.data
            this.response_bookmarkbar = this.response_json.children[0]
            this.response_children = this.response_bookmarkbar.children[0].children
          })
          .catch((err) => {
            console.log(err);
          });
      },
      async reloadFile() {
        console.log(this.content)
        await axios
          .post("reload", {
            item: this.response_json
          })
          .then((res) => {
            console.log(res)
          })
          .catch((err) => {
            console.log(err);
          });
      },
      async downloadFile() {
        await axios
          .post("download", {
            item: this.response_json
          })
          .then((res) => {
            console.log(res.data)
            this.fileDownload(res.data)
          })
          .catch((err) => {
            console.log(err);
          });
      },
      fileDownload(html_text) {
        const blob = new Blob([html_text], {type: "text/html" })
        const link = document.createElement("a");
        link.href = URL.createObjectURL(blob);
        link.download = "bookmark.html";
        link.click();
      }
    }
  }
</script>
