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
  <el-button round color="#9A669B" size="large" @click="downloadFile">
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

let received = "";
const onChangeFile = (e: any) => {
  const file = e.target.files[0];
  const reader = new FileReader();

  reader.readAsDataURL(file, "utf-8");

  reader.onload = async () => {
    const fileTxt = reader.result.slice(22);
    console.log(fileTxt)
    await axios
      .post("html-json", {
        bookmark: fileTxt,
      })
      .then((res) => {
        console.log(res);
      })
      .catch((err) => {
        console.log(err);
      });
  };
};
const downloadFile = () => {
  const blob = new Blob([received], { type: "text/plain" });
  const link = document.createElement("a");
  link.href = URL.createObjectURL(blob);
  link.download = "donwload.html";
  link.click();
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
