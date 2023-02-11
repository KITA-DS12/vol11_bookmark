<template>
  <v-app id="inspire">
    <v-main class="grey lighten-3">
      <v-container style="padding-top: 10%;">
        <v-row>
          <v-col
            cols="12"
            sm="6"
          >
            <v-sheet
              rounded="lg"
              min-height="100%"
              class="grey lighten-3"
              style="text-align: center;"
            >
              <input type="file" ref="input" accept="html" style="display: none" @change="getFileContent">
              <div v-on:click="inputButton">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 20"><path d="M6.5 20Q4.22 20 2.61 18.43 1 16.85 1 14.58 1 12.63 2.17 11.1 3.35 9.57 5.25 9.15 5.88 6.85 7.75 5.43 9.63 4 12 4 14.93 4 16.96 6.04 19 8.07 19 11 20.73 11.2 21.86 12.5 23 13.78 23 15.5 23 17.38 21.69 18.69 20.38 20 18.5 20H13Q12.18 20 11.59 19.41 11 18.83 11 18V12.85L9.4 14.4L8 13L12 9L16 13L14.6 14.4L13 12.85V18H18.5Q19.55 18 20.27 17.27 21 16.55 21 15.5 21 14.45 20.27 13.73 19.55 13 18.5 13H17V11Q17 8.93 15.54 7.46 14.08 6 12 6 9.93 6 8.46 7.46 7 8.93 7 11H6.5Q5.05 11 4.03 12.03 3 13.05 3 14.5 3 15.95 4.03 17 5.05 18 6.5 18H9V20M12 13Z" /></svg>
                <p class="grey--text text--lighten-1 text-button font-weight-bold">
                  <font size="4">Click the BUTTON to Upload</font>
                </p>
              </div>
              <v-btn style="margin-top: 5%" width="70%" rounded class="white--text" color="green lighten-1" x-large @click="inputButton">UPLOAD FILE</v-btn>
            </v-sheet>
          </v-col>
          <v-col
            cols="12"
            sm="6"
          >
            <v-sheet
              min-height="70vh"
              rounded="lg"
              class="grey lighten-3"
              style="text-align: center; position: relative;"
            >
              <v-combobox
                v-model="chips"
                chips
                clearable
                hide-selected
                label="Please enter a name for the folder."
                multiple
                height="300"
              >
                <template v-slot:selection="{ attrs, item, select, selected }">
                  <v-chip
                    class="white--text"
                    color="deep-purple lighten-3"
                    v-bind="attrs"
                    :input-value="selected"
                    close
                    @click="select"
                    @click:close="removeChips(item)"
                  >
                    <strong>{{ item }}</strong>&nbsp;
                  </v-chip>
                </template>
              </v-combobox>
              <v-btn style="position: absolute; right: 20%; bottom: 25%;" rounded class="white--text" color="blue lighten-1" x-large @click="uploadFile">
                EXECUTE
                <v-icon right>
                  mdi-send
                </v-icon>
              </v-btn>
            </v-sheet>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
import axios from "axios";

export default {
  data: () => ({
    content: '',
    response_json: null,
    response_bookmarkbar: null,
    response_children: null,
    chips: []
  }),
  methods: {
    inputButton() { this.$refs.input.click();
    },
    async getFileContent() {
      try {
        const file = this.$refs.input.files[0]
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
      await axios
        .post("upload", {
          bookmark: this.content.slice(22),
          folder: this.chips
        })
        .then((res) => {
          this.$router.push({name:'download', params: {response: res.data}})
        })
        .catch((err) => {
          console.log(err);
        });
    },
  }
}
</script>
<style>
svg {
  fill: #BBB;
  margin: 50px;
}
</style>
