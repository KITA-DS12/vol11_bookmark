from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List,Optional
from category import make_folder_category_list as mf
from utils import BookMark_Json


app = APIRouter()

class JsonPost(BaseModel):
    bookmark: dict = Field({}, description="BookmarkのDict")
    folder: List[str] = Field(["Folder"], description="フォルダー")
    other: str = Field("その他", description="その他のフォルダーの名前")


@app.post(
    "/json-json"
)
async def json_to_json(bookmark_file: JsonPost):
    """Jsonから変換する

    Args:
        file (JsonPost): Schemeを参照

    Returns:
        dict: Bookmark Json
    """
    bookmark_json = BookMark_Json(bookmark_file.bookmark)
    categorize_list = mf(
        book_mark_info_list=bookmark_json.folder_to_list(),
        candidate_labels_list=bookmark_file.folder,
        other_folder_name=bookmark_file.other

    )
    bookmark = bookmark_json.list_to_folder(
        categorise=categorize_list
    )

    return bookmark







