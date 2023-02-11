from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from typing import List
import time
import shutil
import os
from bookmarks_converter import BookmarksConverter
import json
from category import make_folder_category_list as mf
from utils import BookMark_Json
import base64


app = FastAPI()
origins = ["http://localhost:8080"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class Post(BaseModel):
    bookmark : str = Field("Html", description="Base64のHTML")
    folder : List[str] = Field(["Folder"], description="フォルダー")

@app.post(
    "/html-json"
)
async def upload(bookmark_file: Post):
    """bookmarkが保存されたhtmlをjsonに変換する
    形式は以下を参照
    https://github.com/radam9/bookmarks-converter/blob/main/bookmarks_file_structure.md
    """

    path = f"/tmp/{str(time.time())}"
    with open(path, "w+b") as buffer:
        buffer.write(base64.b64decode(bookmark_file.bookmark))

    bookmarks = BookmarksConverter(path)
    bookmarks.parse("html")
    bookmarks.convert("json")
    os.remove(path)

    bookmark_json = BookMark_Json(bookmarks.bookmarks)
    categorize_list = mf(
        book_mark_info_list= bookmark_json.folder_to_list(),
        candidate_labels_list= bookmark_file.folder,
        
    )
    bookmark = bookmark_json.list_to_folder(
        categorise=categorize_list
    )


    return bookmark

@app.post(
    "/json-html",
    response_class=FileResponse
)
async def json_to_html(item : dict):
    """jsonをhtmlに変換する"""
    path = f"/tmp/{str(time.time())}"
    with open(path, "w+b") as buffer:
        buffer.write(json.dumps(item).encode("utf-8"))
    bookmarks = BookmarksConverter(path)
    bookmarks.parse("json")
    bookmarks.convert("html")
    with open(path, "w+b") as buffer:
        buffer.write(bookmarks.bookmarks.encode("utf-8"))
    return FileResponse(path)


