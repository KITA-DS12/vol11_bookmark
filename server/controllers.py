from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
import time
import shutil
import os
from bookmarks_converter import BookmarksConverter
import json


app = FastAPI()
origins = ["http://localhost:8080"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post(
    "/html-json"
)
async def upload(bookmark_file: UploadFile(content_type="text/html", filename="html") = File(...)):
    """bookmarkが保存されたhtmlをjsonに変換する
    形式は以下を参照
    https://github.com/radam9/bookmarks-converter/blob/main/bookmarks_file_structure.md
    """

    path = f"/tmp/{str(time.time())}"
    with open(path, "w+b") as buffer:
        shutil.copyfileobj(bookmark_file.file, buffer)

    bookmarks = BookmarksConverter(path)
    bookmarks.parse("html")
    bookmarks.convert("json")
    os.remove(path)

    return bookmarks.bookmarks

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


