<template>
  <v-app id="inspire">
    <v-main class="red lighten-4">
      <v-card>
        <v-card-title class="teal lighten-1 white--text text-h5">
          <b>BookMark</b>
          <v-spacer />
          <v-btn rounded class="black--text" color="grey lighten-3" x-large @click="reloadFile">
            EXECUTE
            <v-icon dark right>
              mdi-reload
            </v-icon>
          </v-btn>
        </v-card-title>
        <v-row
          class="pa-4 red lighten-5"
          justify="space-between"
        >
          <v-col cols="5">
            <v-treeview
              :active.sync="active"
              :items="response_children"
              item-key="id"
              item-text="title"
              :load-children="fetchFiles"
              :open.sync="open"
              activatable
              color="#CE5D84"
              transition
            >
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

          <v-col
            class="text-center"
          >
            <v-scroll-y-transition mode="out-in">
              <div
                v-if="selected == undefined"
                class="text-h6 grey--text text--lighten-1 font-weight-light"
                style="align-self: center;"
              >
                Select a File
              </div>
              <v-card
                v-else
                :key="selected"
                class="pt-6 mx-auto class red lighten-5"
                flat
              >
                <div v-for="folder in response_children">
                  <div v-for="data in folder.children">
                    <div v-if="data.id == active[0]">
                      <div v-if="data.type == 'url'">
                        <v-avatar size="64">
                          <img :src="data.icon">
                        </v-avatar>
                        <v-row justify="center" style="text-align: center" align-content="center">
                          <v-col cols="12" sm="2">
                            <v-subheader>title</v-subheader>
                          </v-col>
                          <v-col cols="12" sm="6">
                            <v-text-field
                              v-model="data.title"
                              single-line
                              width="30px"
                            ></v-text-field>
                          </v-col>
                        </v-row>
                        <v-row justify="center" style="text-align: center" align-content="center">
                          <v-col cols="12" sm="2">
                            <v-subheader>link</v-subheader>
                          </v-col>
                          <v-col cols="12" sm="6">
                              <div class="textWrap" style="padding-top: 10px;"><a :href="data.url">{{ data.url }}</a></div>
                          </v-col>
                        </v-row>
                      </div>
                    </div>
                  </div>
                </div>
              </v-card>
            </v-scroll-y-transition>
          </v-col>
        </v-row>
      </v-card>
    <v-btn style="position: absolute; right: 10%; bottom: 20%;" rounded class="white--text" color="purple lighten-2" x-large @click="downloadFile">
      DOWNLOAD
      <v-icon right>
        mdi-download
      </v-icon>
    </v-btn>
    </v-main>
  </v-app>
</template>

<script>
import axios from "axios";

const pause = ms => new Promise(resolve => setTimeout(resolve, ms))

export default {
  data: () => ({
    folder: [],
    response_json: null,
    response_children: null,
    active: [],
    open: [],
    files: [],
  }),
  computed: {
    selected() {
      if (!this.active.length) return undefined
      const id = this.active[0]
      console.log("ok", id)
      return id
    }
  },
  created : function(){
    this.folder = this.$route.params.folder
    this.response_json = this.$route.params.response
    this.response_children = this.response_json.children
    console.log(this.response_json)
    console.log(this.response_json)
  },
  methods: {
    async fetchFiles(item) {
      await pause(1500)
      let data = item.children.push(...this.response_children)
      return data
    },
    async reloadFile() {
        console.log(this.content)
        await axios
          .post("json-json", {
            bookmark: this.response_json,
            folder: this.folder,
          })
          .then((res) => {
            this.response_json = res.data
            this.response_children = this.response_json.children
          })
          .catch((err) => {
            console.log(err);
          });
      },
      async downloadFile() {
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
        const blob = new Blob([html_text], {type: "text/html" })
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
</style>
