from urls import app
import uvicorn
import asyncio
import sqlalchemy.sql.default_comparator
from sqlalchemy import *
import torch

async def main():
    config = uvicorn.Config(app = app,port = 8888)
    server = uvicorn.Server(config)
    await server.serve()

if __name__ == '__main__':
    asyncio.run(main())
