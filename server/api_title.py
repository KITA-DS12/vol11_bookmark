from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field
from typing import List,Optional,Dict
import asyncio
from multiprocessing import Pool
from logging import getLogger
import time

from title import run_title

logger = getLogger("uvicorn").getChild("ai")

app = APIRouter()

class TitlePost(BaseModel):
    """Title変換のUploadの形式"""
    bookmark: dict = Field(
        {},description="BookmarkのDict"
    )

class TitleReturn(BaseModel):
    """Title変換のReturnの形式"""
    processing : bool
    id : Optional[int] = Field(0, description="ID")
    url_to_list : Optional[str] = Field("Title", description="スクレイピングの結果")
    summary : Optional[str] = Field("まとめ", description="タイトル")

class Not_Found(BaseModel):
    detail : str = Field("Not Found", description="Message")

jobs : Dict[str, TitleReturn] = {}

def suggestion_by_ai(title) -> TitleReturn:
    """AIにtitleをおすすめしてもらう"""
    logger.info("Start generate title")
    loop = asyncio.new_event_loop()
    result = loop.run_until_complete(
        run_title(title)
    )
    ans = TitleReturn(processing = False,id = result[0], url_to_list = result[1], summary = result[2])
    return ans


def title_processing(bookmark : TitlePost, id : str) -> None:
    """AIにタイトルを出してもらう"""
    logger.info("Start Title Process id:{}".format(id))
    jobs[id] = TitleReturn(processing=True)
    p = Pool(1)
    bookmark_return = suggestion_by_ai(bookmark)
    logger.info("Ended AI Process id:{}".format(id))

    jobs[id] = bookmark_return

@app.post(
    "/title-post",
    status_code=202
)
async def title_post(background : BackgroundTasks,
                     bookmark : TitlePost) -> str:
    """Titleのおすすめを返す

    Args:
        bookmark (TitlePost): Schemeを参照
    Returns:
        string : Request ID
    """    
    job_id = str(time.time()).replace(".","-")
    background.add_task(
        title_processing,
        bookmark,      
        job_id
    )

    return job_id

@app.get(
    "/title_get/{id}",
    responses = {404: {"model" : Not_Found}}
)
async def result(id : str) -> TitleReturn:
    """現在のJOBのステータスを返す

    Args:
        id (str): Request ID

    Returns:
        TitleReturn: Schemeを参照
    """
    task : TitleReturn = jobs.get(id)
    if task == None:
        raise HTTPException(404, detail="Job is not found.")

    if task.processing == False:
        jobs.pop(id)

    return task



    








