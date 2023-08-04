
# Unpakcer

Categorize browser bookmarks and Suggest site title.

[![GPLv3 License](https://img.shields.io/badge/License-GPL%20v3-yellow.svg)](https://opensource.org/licenses/)

![Logo](https://github.com/KITA-DS12/vol11_bookmark/raw/main/src/assets/logo.png)

## Demo

Please click on the thumbnails

[![Demo Movie](http://img.youtube.com/vi/GBR4Z58Ww-8/sddefault.jpg)](https://www.youtube.com/watch?v=GBR4Z58Ww-8)

## Features

- Categorize Bookmarks
- Generate titltes automatically by summary of text
- Importing multiple browser Bookmarks
- Editing Bookmarks
- Site Preview
- Support Chromium based browser and Firefox

## Run Locally

### Dependencies

- Docker
- Docker-Compose
- At least 16 GB memory

### Recommends

- Nvidia Container Toolkit
- npm
- GPU with CUDA support
- 32GB memory

### Run on Docker (Recommend)

Clone the project

```bash
  git clone https://github.com/KITA-DS12/vol11_bookmark
```

Go to the project directory

```bash
  cd vol11_bookmark
```

Obtain [linkpreview's](https://www.linkpreview.net/) API Key

```bash
  echo VUE_APP_API_KEY={YOUR API KEY} > .env.local
```

Run Docker

```bash
  docker-compose up 
```

You can now access unpacker on localhost:8080

### Run on Electron (Experimental)

Clone the project

```bash
  git clone https://github.com/KITA-DS12/vol11_bookmark
```

Go to the project directory

```bash
  cd vol11_bookmark
```

Obtain [linkpreview's](https://www.linkpreview.net/) API Key

```bash
  echo VUE_APP_API_KEY={YOUR API KEY} > .env.local
```

Run Server

```bash
  docker-compose up server -d
```

Install Dependencies

```bash
  npm install
```

Run Electron

```bash
  yarn run electron:serve
```

## Usage

1. Export your bookmark html file from your browser.
1. Upload Bookmark File.
1. Choose Target Folder.
1. Enter Category.
1. Modify Your Bookmark.
1. Download Categorized Bookmark HTML file.
1. Import HTML file to your browser.

## FAQ

#### vue-cli-service not found when starting server

Run follow command in local.

```bash
npm install @vue/cli
```

## Tech Stack

**Client:** Vue.js, Vuetify

**Server:** FastAPI, Pytorch, Transformer, HuggingFace

## Acknowledgements

- [README Editor](https://readme.so/ja/editor)
- [Geek Project](https://biz.supporterz.jp/geekpjt/)
- [Geek Camp](https://talent.supporterz.jp/geekcamp/)

We used the following Model

- [Categorize Model](https://huggingface.co/MoritzLaurer/mDeBERTa-v3-base-mnli-xnli)
- [Generate Title Model](https://huggingface.co/csebuetnlp/mT5_multilingual_XLSum)


## Citation

- Laurer, Moritz, Wouter van Atteveldt, Andreu Salleras Casas, and Kasper Welbers. 2022. ‘Less Annotating, More Classifying – Addressing the Data Scarcity Issue of Supervised Machine Learning with Deep Transfer Learning and BERT - NLI’. Preprint, June. Open Science Framework. https://osf.io/74b8k.

- Hasan, T., Bhattacharjee, A., Islam, M., Mubasshir, K., Li, Y.F., Kang, Y.B., Rahman, M., & Shahriyar, R. (2021). XL-Sum: Large-Scale Multilingual Abstractive Summarization for 44 Languages. In Findings of the Association for Computational Linguistics: ACL-ĲCNLP 2021 (pp. 4693–4703). Association for Computational Linguistics.https://aclanthology.org/2021.findings-acl.413


## License

[GNU General Public License v3.0](https://github.com/KITA-DS12/vol11_bookmark/blob/main/LICENSE)
