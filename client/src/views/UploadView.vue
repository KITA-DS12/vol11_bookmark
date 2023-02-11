<template>
  <v-app>
    <div class="main">
    <div class="input-file">
    <h1>ファイルを入力してください</h1>
  <v-file-input v-model="file" accept="text/html" truncate-length="15"></v-file-input>

  <br/>

  <h1>フォルダのリストを入力してください</h1>
  <v-combobox v-model="chips" :items="items" chips clearable label="フォルダのタグを追加" multiple
    prepend-icon="mdi-filter-variant" solo>
    <template v-slot:selection="{ attrs, item, select, selected }">
      <v-chip v-bind="attrs" :input-value="selected" close @click="select" @click:close="remove(item)">
        <strong>{{ item }}</strong>&nbsp;
        <span>(tag)</span>
      </v-chip>

    </template>
  </v-combobox>
  <v-btn v-on:click="clicked" class="submit">送信</v-btn>

  </div>
  </div>
</v-app>

</template>

<script>
export default {
  data() {
    return {
      // 送信するファイル
      file: "",
      // この配列をtagとして送信する
      chips: ['大学', '研究', 'ゲーム', 'その他'],
      items: ['数学', '競技プログラミング','圏論','論理学','地理','言語学'],
    }
  },

  methods: {
    remove(item) {
      this.chips.splice(this.chips.indexOf(item), 1)
    },
    // TODO:タグとファイルを送信する
    clicked(){
      console.log("送信")
    },
  },
}

</script>

<style scoped>
.main {
  text-align: center;
}
/* .input-file {
  text-align: center;
  width: 1110px;
} */


</style>
