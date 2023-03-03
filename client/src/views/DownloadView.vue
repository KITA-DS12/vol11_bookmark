<template>
  <v-app id="inspire">
    <v-main class="red lighten-4">
      <v-card>
        <v-dialog v-model="dialogExec">
          <v-card>
            <v-card-title>Select target folder</v-card-title>
            <v-divider></v-divider>
            <v-card-text>
              <div style="height: 10vh" />
              <v-combobox v-model="targets" :items="folders" hide-selected multiple
                label="Select the target folder for classification." @input="onInputCombobox">
                <template v-slot:selection="{ attrs, item, parent, selected }">
                  <v-chip v-bind="attrs" color="pink lighten-2" text-color="white" :input-value="selected" label>
                    <span class="pr-2">
                      {{ item }}
                    </span>
                    <v-icon small @click="parent.selectItem(item)">
                      $delete
                    </v-icon>
                  </v-chip>
                </template>
              </v-combobox>
              <v-combobox v-model="chips" clearabkle hide-selected label="Please enter a name for the folder." multiple
                height="300">
                <template v-slot:selection="{ attrs, item, select, selected }">
                  <v-chip class="white--text" color="deep-purple lighten-2" v-bind="attrs" :input-value="selected" close
                    @click="select" @click:close="removeChips(item)" label>
                    <strong>{{ item }}</strong>&nbsp;
                  </v-chip>
                </template>
              </v-combobox>
            </v-card-text>
            <v-divider></v-divider>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="blue darken-1" text @click="dialogExec = false">
                Close
              </v-btn>
              <v-btn color="blue darken-1" text @click="reloadFile">
                EXEC
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
        <v-dialog v-model="dialogMove" scrollable max-width="300px">
          <v-card>
            <v-card-title>Move a file</v-card-title>
            <v-divider></v-divider>
            <v-card-text style="height: 300px;">
              <v-treeview :active.sync="active_dialog" :items="unpacker_json" item-key="id" item-text="title"
                :load-children="fetchFiles" item-disabled activatable color="#CE5D84" transition :return-object="true"
                expand-icon="">
                <template v-slot:prepend="{ item }">
                  <v-icon v-if="item.children">
                    mdi-folder
                  </v-icon>
                </template>
              </v-treeview>
            </v-card-text>
            <v-divider></v-divider>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="blue darken-1" text @click="dialogMove = false">
                Close
              </v-btn>
              <v-btn color="blue darken-1" text @click="moveFile">
                Save
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
        <v-card-title class="teal lighten-1 white--text text-h5" style="padding-top: 3px;">
          <b>BookMark</b>
          <v-spacer />
          <v-btn rounded class="black--text" color="grey lighten-3" x-large @click="dialogExec = true">
            EXECUTE
            <v-icon dark right>
              mdi-reload
            </v-icon>
          </v-btn>
        </v-card-title>
        <v-row class="pa-4 red lighten-5" justify="space-between">
          <v-col cols="5">
            <v-treeview :active.sync="active" :items="unpacker_json" item-key="id" item-text="title"
              :load-children="fetchFiles" :open.sync="open" activatable color="#CE5D84" transition
              :return-object="true">
              <template v-slot:prepend="{ item }">
                <v-icon v-if="!item.children">
                  mdi-file
                </v-icon>
                <v-icon v-if="item.children">
                  mdi-folder
                </v-icon>
              </template>
              <template v-slot:append="{ item }">
                <v-btn v-if="!item.children" fab small depressed color="grey lighten-5" @click="dialogMove = true">
                  <v-icon>
                    mdi-file-move-outline
                  </v-icon>
                </v-btn>
                <v-icon v-if="item.children">
                  mdi-pencil
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
                <div v-if="selected.type == 'url'">
                  <v-avatar size="64">
                    <img :src="selected.icon">
                  </v-avatar>
                  <v-row justify="center" style="text-align: center" align-content="center">
                    <v-col cols="12" sm="2">
                      <v-subheader style="margin-top: 12px;">title</v-subheader>
                    </v-col>
                    <v-col cols="12" sm="6">
                      <v-text-field v-model="selected.title" single-line width="30px"></v-text-field>
                    </v-col>
                    <v-col cols="12" sm="2">
                      <v-btn small rounded style="margin-top: 17px;" class="white--text" color="deep-purple lighten-2"
                        @click="generateTitle(selected)">
                        <v-icon>
                          mdi-brain
                        </v-icon>
                        Generate
                      </v-btn>
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
                    <v-col cols="12" sm="2">
                    </v-col>
                  </v-row>
                  <div style="height: 60px" />
                  <v-row justify="center" style="text-align: center" align-content="center">
                    <v-card class="mx-auto" max-width="344" color="#FAFAFA" flat>
                      <v-img id="previewImg" :src="previewImg" height="200px" cover></v-img>
                      <v-card-title id="previewTitle"> {{ previewTitle }} </v-card-title>
                      <v-card-subtitle id="previewDescription"> {{ previewDescription }} </v-card-subtitle>
                    </v-card>
                  </v-row>
                  <div style="height: 60px" />
                </div>
              </v-card>
            </v-scroll-y-transition>
          </v-col>
        </v-row>
        <v-btn rounded style="position: fixed; bottom: 10%; right: 5%;" class="white--text" color="purple lighten-2"
          x-large @click="downloadFile">
          DOWNLOAD
          <v-icon right>
            mdi-download
          </v-icon>
        </v-btn>
      </v-card>
    </v-main>
    <v-progress-circular v-if="req_id != null || gen_id != null" :size="70" :width="7" color="purple" indeterminate
      style="position: fixed; bottom: 50%; right: 45%;">
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
    unpacker_json: null,
    active: [],
    active_dialog: [],
    open: [],
    files: [],
    req_id: null,
    gen_id: null,
    selectFolder: '',
    dialogMove: false,
    dialogExec: false,
    folders: [],
    targets: [],
    previewTitle: "",
    previewDescription: "",
    previewImg: "",
  }),
  computed: {
    selected() {
      if (!this.active.length) return undefined
      if (this.active[0].type == "url") {
        this.previewTitle = ""
        this.previewImg = ""
        this.previewDescription = ""
        this.fetchPreview()
      }
      return this.active[0]
    }
  },
  created: function () {
    this.chips = this.$route.params.chips
    this.response_json = this.$route.params.response
    this.response_children = this.response_json.children
    this.response_children.forEach(element => {
      console.log(element)
      if (element.title == "unpacker") {
        this.unpacker_json = element.children
      } else {
        console.log("else")
      }
    })
    this.unpacker_json.forEach((folder) => {
      console.log(folder)
      if (folder.type == "folder" && folder.children.length != 0) {
        console.log(folder.title)
        this.folders.push(folder.title)
      }
    })
    this.targets = this.folders
  },
  methods: {
    onInputCombobox() {
      this.$nextTick(() => {
        // 入力値が選択肢にあるかチェックします。
        let isExist = false;
        for (let folder of this.folders) {
          if (this.targets[this.targets.length - 1] == folder) {
            isExist = true;
            break;
          }
        }

        // 入力値が選択肢にない場合
        if (!isExist) {
          // 入力値をクリアします。
          this.targets.pop()
        }
      })
    },
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
      this.previewTitle = json.title;
      this.previewImg = json.image;
      this.previewDescription = json.description;
    },
    async fetchFiles(item) {
      await pause(1500)
      let data = item.children.push(...this.response_children)
      return data
    },
    moveFile() {
      console.log(this.active[0])
      console.log(this.active_dialog[0])
      this.unpacker_json.forEach((folder) => {
        console.log(folder)
        folder.children.forEach((file, idx) => {
          console.log(file, idx)
          if (file.type == "url" && file.id == this.active[0].id) {
            this.active_dialog[0].children.push(this.active[0])
            folder.children.splice(idx, 1)
          }
        })
      })
    },
    async reloadFile() {
      this.dialogExec = false
      await axios
        .post("json-json", {
          bookmark: this.response_json,
          folder: this.chips,
          other: "その他",
          target: this.targets,
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
            this.response_children.forEach(element => {
              if (element.title == "unpacker") {
                this.unpacker_json = element.children
              }
            })
            this.folders = []
            this.targets = []
            this.unpacker_json.forEach((folder) => {
              console.log(folder)
              if (folder.type == "folder" && folder.children.length != 0) {
                console.log(folder.title)
                this.folders.push(folder.title)
              }
            })
            this.targets = this.folders
            this.req_id = null
          }
        })
        .catch((err) => {
          console.log(err);
        });
    },
    async generateTitle(selected_json) {
      console.log(selected_json)
      await axios
        .post("title-post", {
          bookmark: selected_json
        })
        .then((res) => {
          console.log(res.data)
          this.gen_id = res.data
          this.waitForGenerating()
        })
        .catch((err) => {
          console.log(err);
        });
    },
    async waitForGenerating() {
      console.log(this.gen_id)
      await axios
        .get(`title_get/${this.gen_id}`, {
        })
        .then((res) => {
          console.log(res.data)
          if (res.data.processing) {
            setTimeout(this.waitForGenerating, 2000)
          }
          else {
            this.active[0].title = res.data.summary
            this.gen_id = null
          }
        })
        .catch((err) => {
          console.log(err);
          setTimeout(this.waitForGenerating, 2000)
        });
    },
    async downloadFile() {
      console.log(this.response_children)
      this.response_children.forEach(element => {
        console.log(element)
        if (element.title == "unpacker") {
          this.unpacker_json == element.children
        }
      })
      console.log(this.unpacker_json)
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
    removeChips(item) {
      this.chips.splice(this.chips.indexOf(item), 1)
    }
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
