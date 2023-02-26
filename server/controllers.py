from fastapi import FastAPI, File, UploadFile, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
import time
import shutil
import os
from bookmarks_converter import BookmarksConverter
import json
import base64
from typing import List
from dictknife import deepmerge
from api_convert import app as api_convert_router
from utils import BookMark_Json


app = FastAPI()
origins = ["http://localhost:8080"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api_convert_router)


class Post(BaseModel):
    bookmark: List[str] = Field(["HTML"], description="Base64のHTML")


@app.post(
    "/html-json"
)
async def upload(bookmark_file: Post) -> dict:
    """bookmarkが保存されたhtmlをjsonに変換する。\n
    AIによる処理はここでは行わない
    形式は以下を参照
    https://github.com/radam9/bookmarks-converter/blob/main/bookmarks_file_structure.md
    """
    result = {}


    for bookmark in bookmark_file.bookmark:
        path = f"/tmp/{str(time.time())}"
        with open(path, "w+b") as buffer:
            buffer.write(base64.b64decode(bookmark))

        bookmarks = BookmarksConverter(path)
        bookmarks.parse("html")
        bookmarks.convert("json")
        os.remove(path)
        result = deepmerge(result, bookmarks.bookmarks)


    return result



def delete_file(path: str) -> None:
    time.sleep(5)
    os.remove(path)


@app.post(
    "/json-html",
    response_class=FileResponse
)
async def json_to_html(item: dict, background : BackgroundTasks):
    """jsonをhtmlに変換する"""
    bookmark = BookMark_Json(item)
    item = bookmark.sort_id()
    path = f"/tmp/{str(time.time())}"
    with open(path, "w+b") as buffer:
        buffer.write(json.dumps(item).encode("utf-8"))
    bookmarks = BookmarksConverter(path)
    bookmarks.parse("json")
    bookmarks.convert("html")
    with open(path, "w+b") as buffer:
        buffer.write(bookmarks.bookmarks.encode("utf-8"))
    background.add_task(delete_file, path)
    return FileResponse(path)


@app.post(
    "/base64"
)
async def base6464(file: UploadFile = File(...)):
    """ファイルに対してBase64 Encodeを行う"""
    path = f"/tmp/{str(time.time())}"
    with open(path, "w+b") as buffer:
        shutil.copyfileobj(file.file, buffer)
    with open(path, "rb") as f:
        return base64.b64encode(f.read())
