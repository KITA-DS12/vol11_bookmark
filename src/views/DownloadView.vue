<template>
  <v-app id="inspire">
    <v-main class="red lighten-4">
      <v-card>
        <v-card-title class="teal lighten-1 white--text text-h5" style="padding-top: 3px;">
          <b>BookMark</b>
          <v-spacer />
          <v-btn rounded class="black--text" color="grey lighten-3" x-large @click="reloadFile">
            EXECUTE
            <v-icon dark right>
              mdi-reload
            </v-icon>
          </v-btn>
        </v-card-title>
        <v-row class="pa-4 red lighten-5" justify="space-between">
          <v-col cols="5">
            <v-treeview :active.sync="active" :items="response_children" item-key="id" item-text="title"
              :load-children="fetchFiles" :open.sync="open" activatable color="#CE5D84" transition :return-object="true">
              <template v-slot:prepend="{ item }">
                <v-icon v-if="!item.children">
                  mdi-file
                </v-icon>
                <v-icon v-if="item.children">
                  mdi-folder
                </v-icon>
              </template>
            </v-treeview>
          </v-col>
          <v-divider vertical></v-divider>

          <v-col class="text-center">
            <v-scroll-y-transition mode="out-in">
              <div v-if="selected == undefined" class="text-h6 grey--text text--lighten-1 font-weight-light"
                style="align-self: center;">
                Select a File
              </div>
              <v-card v-else style="width: 50vw" class="pt-6 mx-auto class red lighten-5" flat>
                <div v-if="selected.type=='folder'">
                  folder
                </div>
                <div v-if="selected.type=='url'">
                  <v-avatar size="64">
                    <img :src="selected.icon">
                  </v-avatar>
                  <v-row justify="center" style="text-align: center" align-content="center">
                    <v-col cols="12" sm="2">
                      <v-subheader>title</v-subheader>
                    </v-col>
                    <v-col cols="12" sm="6">
                      <v-text-field v-model="selected.title" single-line width="30px"></v-text-field>
                    </v-col>
                  </v-row>
                  <v-row justify="center" style="text-align: center" align-content="center">
                    <v-col cols="12" sm="2">
                      <v-subheader>link</v-subheader>
                    </v-col>
                    <v-col cols="12" sm="6">
                      <div class="textWrap" style="padding-top: 10px;"><a :href="selected.url">{{ selected.url }}</a>
                      </div>
                    </v-col>
                  </v-row>
                  <div style="height: 60px" />
                  <v-row justify="center" style="text-align: center" align-content="center">
                    <v-card
                      class="mx-auto"
                      max-width="344"
                      color="#FAFAFA"
                      flat
                    >
                      <v-img
                        id="previewImg"
                        src=""
                        height="200px"
                        cover
                      ></v-img>
                      <v-card-title id="previewTitle" />

                      <v-card-subtitle id="previewDescription" />
                    </v-card>
                  </v-row>
                  <div style="height: 60px" />
                </div>
              </v-card>
            </v-scroll-y-transition>
          </v-col>
        </v-row>
        <v-btn rounded style="position: fixed; bottom: 10%; right: 5%;" class="white--text" color="purple lighten-2" x-large @click="downloadFile">
          DOWNLOAD
          <v-icon right>
            mdi-download
          </v-icon>
        </v-btn>
      </v-card>
    </v-main>
    <v-progress-circular
      v-if="req_id!=null"
      :size="70"
      :width="7"
      color="purple"
      indeterminate
      style="position: fixed; bottom: 50%; right: 45%;"
    >
    </v-progress-circular>
  </v-app>
</template>

<script>
import axios from "axios";

const pause = ms => new Promise(resolve => setTimeout(resolve, ms))

export default {
  data: () => ({
    chips: [],
    response_json: null,
    response_children: null,
    active: [],
    open: [],
    files: [],
    req_id: null,
  }),
  computed: {
    selected() {
      if (!this.active.length) return undefined
      if (this.active[0].type=="url") {
        this.fetchPreview()
      }
      return this.active[0]
    }
  },
  created: function () {
    this.chips = this.$route.params.chips
    this.response_json = this.$route.params.response
    this.response_children = this.response_json.children
  },
  methods: {
    async fetchPreview() {
      await fetch('https://api.linkpreview.net', {
        method: 'POST',
        mode: 'cors',
        body: JSON.stringify({
          key: process.env.VUE_APP_API_KEY,
          q: this.active[0].url
        })
      })
      .then(data => data.json())
      .then(json => this.createIMG(json))
    },
    createIMG(json) {
      console.log(json)
      document.querySelector('#previewTitle').textContent = json.title;
      document.querySelector('#previewImg').src = json.image;
      document.querySelector('#previewDescription').textContent = json.description;
    },
    async fetchFiles(item) {
      await pause(1500)
      let data = item.children.push(...this.response_children)
      return data
    },
    async reloadFile() {
      await axios
        .post("json-json", {
          bookmark: this.response_json,
          folder: this.chips,
          other: "その他",
          target: this.chips,
        })
        .then((res) => {
          this.req_id = res.data
          this.waitForProcessing()
        })
        .catch((err) => {
          console.log(err);
        });
    },
    async waitForProcessing() {
      await axios
        .get(`json-json/${this.req_id}`, {
        })
        .then((res) => {
          if (res.data.processing) {
            setTimeout(this.waitForProcessing, 3000)
          }
          else {
            this.response_json = res.data.bookmark
            this.response_children = this.response_json.children
            this.req_id = null
          }
        })
        .catch((err) => {
          console.log(err);
        });
    },
    async downloadFile() {
      console.log(this.response_json)
      await axios
        .post("json-html", {
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
      const blob = new Blob([html_text], { type: "text/html" })
      const link = document.createElement("a");
      link.href = URL.createObjectURL(blob);
      link.download = "bookmark.html";
      link.click();
    },
  }
}
</script>
<style>
svg {
  fill: #BBB;
  margin: 50px;
}
.textWrap {
  width: 220px;
  white-space:nowrap;
  overflow:hidden;
  text-overflow:ellipsis;
}
.fixed_btn {
  position: fixed;
  bottom: 10%;
  right: 10%;
}
