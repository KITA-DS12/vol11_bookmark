from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field
from typing import List,Optional,Dict
from category import make_folder_category_list as mf
from utils import BookMark_Json
import asyncio
from logging import getLogger
from multiprocessing import Pool
import time


app = APIRouter()

logging = getLogger("uvicorn").getChild("ai")



class JsonPost(BaseModel):
    bookmark: dict = Field({}, description="BookmarkのDict")
    folder: List[str] = Field(["Folder"], description="フォルダー")
    other: Optional[str] = Field("その他", description="その他のフォルダーの名前")
    target : Optional[List[str]] = Field([""], description="対象のフォルダー(Defalt = root)")

class JsonReturn(BaseModel):
    bookmark: Optional[dict] = Field({}, description="BookmarkのDict")
    processing : bool = Field(True, description="サーバーにて処理中かどうか")

class Not_Found(BaseModel):
    detail : str = Field("Not Found", description="Message")

jobs : Dict[str, JsonReturn] = {}
def sort_by_ai(bookmark_file : JsonPost, target_folder : list) -> dict:
    """AIにSORTしてもらう"""
    target_folder = set(target_folder)
    logging.info("Start Sort")
    bookmark_json = BookMark_Json(bookmark_file.bookmark)
    loop = asyncio.new_event_loop()
    book_mark_info_list = bookmark_json.folder_to_list(folder_name=target_folder)
    categorize_list = loop.run_until_complete(mf(
        book_mark_info_list=book_mark_info_list,
        candidate_labels_list=bookmark_file.folder,
        other_folder_name=bookmark_file.other

    ))
    bookmark = bookmark_json.list_to_folder(
        categorise=categorize_list,
        target_folder=target_folder
    )
    logging.info("End Sort")
    return bookmark

def wrap_sort(sort):
    """sort_by_aiのwrap関数"""
    result = sort_by_ai(*sort)
    return result


    

def ai_processing(bookmark_file : JsonPost,id : str) -> None:
    """AIに分類してもらう"""
    logging.info("Start AI Process id:{}".format(id))
    bookmark = []

    jobs[id] = JsonReturn(bookmark={}, processing=True)
    args = [(bookmark_file, bookmark_file.target)]
    p = Pool(1)
    bookmark = p.map(wrap_sort, args)


    logging.info("Ended AI Process id:{}".format(id))

    jobs[id] = JsonReturn(bookmark=bookmark[0], processing=False)




@app.post(
    "/json-json",
    status_code=202   
)
async def json_to_json(background : BackgroundTasks,bookmark_file: JsonPost) -> str:
    """JSONのAIを使用して処理するリクエストを発行する

    Args:
        file (JsonPost): Schemeを参照

    Returns:
        string: Request ID
    """
    job_id = str(time.time()).replace(".","-")
    background.add_task(
        ai_processing,
        bookmark_file,
        job_id
    )
    jobs[job_id] = JsonReturn(bookmark = None, processing=True)

    return job_id

    
@app.get(
    "/json-json/{id}",
    responses = {404: {"model" : Not_Found}}
)
async def result(id : str) -> JsonReturn:
    """現在のJOBのステータスを返す

    Args:
        id (str): Request ID

    Returns:
        JsonReturn: Schemeを参照
    """
    task : JsonReturn = jobs.get(id)
    if task == None:
        raise HTTPException(404, detail="Job is not found.")

    if task.processing == False:
        jobs.pop(id)

    return task
        

    


    








