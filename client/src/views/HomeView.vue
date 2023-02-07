<template>
  <img id="logo" src="@/assets/logo_long.png" alt="" />
  <br />
  <el-button round color="#5A9090" size="large" class="upload-btn">
    <label for="upload-button">
      Upload
      <el-icon>
        <Upload />
      </el-icon>
      <input
        type="file"
        accept=".html"
        id="upload-button"
        @change="onChangeFile"
      />
    </label>
  </el-button>
  <el-button round color="#9A669B" size="large">
    <label>
      Download
      <el-icon>
        <Download />
      </el-icon>
    </label>
  </el-button>
</template>
<script setup lang="ts">
import axios from "axios";
const onChangeFile = (e: any) => {
  const file = e.target.files[0];
  const reader = new FileReader();

  reader.readAsText(file);

  reader.onload = async () => {
    const fileTxt = reader.result;
    await axios.post("upload", {
      content: fileTxt,
    });
  };
};
</script>
<style>
#logo {
  padding: 20px;
  width: 30%;
}

label {
  font-size: 14px;
  padding: 20px 10px 20px 10px;
}

#upload-button {
  display: none;
}

.upload-btn {
  margin-right: 20px;
}
</style>
