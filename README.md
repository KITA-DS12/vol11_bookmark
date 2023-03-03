![unpacker](./src/assets/logo.png)
Categorize browser bookmarks and Suggest site title.

## Support Browser
- Google Chrome
- Microsoft Edge
- Opera

Oher Chromium based Browser

## Run (Linux x86)(electron)
1. download Pakage from release page.
1. unzip
1. run this command
```bash
$ python3 -m venv /tmp/venv
$ source /tmp/venv/bin/activate
$ python3 -m pip install -r src/server/requirements.txt
$ /tmp/venv/bin/python ./src/server/main.py
```
1. run `node_modules/dist_electron/client-0.1.0.AppImage`

## Run in Docker
1. Clone this repository.
1. Run command.
``` bash
$ docker-compose up -d
```
1. Aceess `localhost:8080` on your browser.

## Usage
1. Export your bookmark html file from your browser.
1. Upload Bookmark File.
1. Choose Target Folder.
1. Enter Category.
1. Modify Your Bookmark.
1. Download Categorized Bookmark HTML file.
1. Import HTML file to your browser.

## About Model
分類分けではモデルをお借りしました。(https://huggingface.co/google/tapas-small-finetuned-wtq)  

タイトルおすすめではモデルをお借りしました。(https://huggingface.co/csebuetnlp/mT5_multilingual_XLSum)

## License

See 
[License][def]

[def]: ./LICENSE