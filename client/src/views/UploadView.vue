<template>
  <v-app>
    <div class="main">
    <div class="input-file">
    <h1>ファイルを入力してください</h1>
  <v-file-input truncate-length="15"></v-file-input>
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
  <div class="send-wrapper"><v-btn class="submit">送信</v-btn></div>
  
  </div>
  </div>
</v-app>
  
</template>

<script>
  import HelloWorld from '../components/HelloWorld'

  export default {
    name: 'Home',

    components: {
      HelloWorld,
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
