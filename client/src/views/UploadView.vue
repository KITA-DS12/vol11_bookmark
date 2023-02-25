<template>
  <v-app id="inspire">
    <v-main class="red lighten-4">
      <v-container style="padding-top: 10%;">
        <v-row>
          <v-col
            cols="12"
            sm="6"
          >
            <v-sheet
              rounded="lg"
              min-height="100%"
              class="red lighten-4"
              style="text-align: center;"
            >
              <input type="file" ref="input" accept="html" style="display: none" @change="getFileContent">
              <svg style="fill: #555;" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 20"><path d="M6.5 20Q4.22 20 2.61 18.43 1 16.85 1 14.58 1 12.63 2.17 11.1 3.35 9.57 5.25 9.15 5.88 6.85 7.75 5.43 9.63 4 12 4 14.93 4 16.96 6.04 19 8.07 19 11 20.73 11.2 21.86 12.5 23 13.78 23 15.5 23 17.38 21.69 18.69 20.38 20 18.5 20H13Q12.18 20 11.59 19.41 11 18.83 11 18V12.85L9.4 14.4L8 13L12 9L16 13L14.6 14.4L13 12.85V18H18.5Q19.55 18 20.27 17.27 21 16.55 21 15.5 21 14.45 20.27 13.73 19.55 13 18.5 13H17V11Q17 8.93 15.54 7.46 14.08 6 12 6 9.93 6 8.46 7.46 7 8.93 7 11H6.5Q5.05 11 4.03 12.03 3 13.05 3 14.5 3 15.95 4.03 17 5.05 18 6.5 18H9V20M12 13Z" /></svg>
              <p class="grey--text text--darken-2 text-button font-weight-bold">
                <font size="4">1. Click the BUTTON to Upload</font>
              </p>
              <v-btn style="margin-top: 5%" width="70%" rounded class="white--text" color="teal lighten-1" x-large @click="inputButton">UPLOAD FILE</v-btn>
            </v-sheet>
          </v-col>
          <v-col
            cols="12"
            sm="6"
          >
            <v-sheet
              min-height="70vh"
              rounded="lg"
              class="red lighten-4"
              style="text-align: center; position: relative;"
            >
              <div style="height: 10vh" />
              <v-combobox
                v-model="targets"
                :items="folders"
                hide-selected
                multiple
                label="2. Select the target folder for classification."
                @input="onInputCombobox"
              >
                <template v-slot:selection="{ attrs, item, parent, selected }">
                  <v-chip
                    v-bind="attrs"
                    color="pink lighten-2"
                    text-color="white"
                    :input-value="selected"
                    label
                  >
                    <span class="pr-2">
                      {{ item }}
                    </span>
                    <v-icon
                      small
                      @click="parent.selectItem(item)"
                    >
                      $delete
                    </v-icon>
                  </v-chip>
                </template>
              </v-combobox>
              <v-combobox
                v-model="chips"
                clearabkle
                hide-selected
                label="3. Please enter a name for the folder."
                multiple
                height="300"
              >
                <template v-slot:selection="{ attrs, item, select, selected }">
                  <v-chip
                    class="white--text"
                    color="deep-purple lighten-2"
                    v-bind="attrs"
                    :input-value="selected"
                    close
                    @click="select"
                    @click:close="removeChips(item)"
                    label
                  >
                    <strong>{{ item }}</strong>&nbsp;
                  </v-chip>
                </template>
              </v-combobox>
              <v-btn v-bind:disabled="!isAllowedToPush" style="position: fixed; bottom: 10%; right: 5%;" rounded class="white--text" color="teal lighten-1" x-large @click="uploadFile">
                EXECUTE
                <v-icon right>
                  mdi-send
                </v-icon>
              </v-btn>
            </v-sheet>
          </v-col>
        </v-row>
      </v-container>
      <v-progress-circular
        v-if="req_id!=null"
        :size="70"
        :width="7"
        color="purple"
        indeterminate
        style="position: fixed; bottom: 50%; right: 45%;"
      >
      </v-progress-circular>
    </v-main>
  </v-app>
</template>

<script>
import axios from "axios";

export default {
  data: () => ({
    content: '',
    response_json: null,
    chips: [],
    other: "その他",
    folders: [],
    targets: [],
    req_id: null,
  }),
  computed: {
    isAllowedToPush() {
      if (this.content != '' && this.chips.length != 0 && this.req_id == null) {
        return true;
      } else {
        return false;
      }
    }
  },
  methods: {
    onInputCombobox() {
      this.$nextTick(() => {
        // 入力値が選択肢にあるかチェックします。
        let isExist = false;
        for (let folder of this.folders) {
          if (this.targets[this.targets.length-1] == folder) {
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
    inputButton() { this.$refs.input.click();
    },
    async getFileContent() {
      try {
        const file = this.$refs.input.files[0]
        const content = await this.readFileAsync(file)
        this.content = content
        await this.readFolder()
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
    async readFolder() {
      await axios
        .post("html-json", {
          bookmark: [this.content.slice(22)],
        })
        .then((res) => {
          this.response_json = res.data
          const children = res.data.children[0].children[0].children
          children.forEach((elem, index) => {
            if (elem.type == "folder") {
              this.folders.push(elem.title)
            }
          })
          this.targets = this.folders
        })
        .catch((err) => {
          console.log(err);
        });
    },
    async uploadFile() {
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
            setTimeout(this.waitForProcessing, 1500)
          }
          else {
            console.log(res.data.bookmark)
            this.$router.push({name:'download', params: {response: res.data.bookmark, folder: this.chips}})
          }
        })
        .catch((err) => {
          console.log(err);
        });
    },
    removeChips(item) {
      this.chips.splice(this.chips.indexOf(item), 1)
    }
  }
}
</script>
<style>
svg {
  fill: #555;
  margin: 50px;
}
</style>
