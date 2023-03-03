import sys
from cx_Freeze import setup, Executable
base  = None

exe = Executable(script = "main.py",base = base)
build_exe_options = {
    "packages": [
        "sqlalchemy",
        "uvicorn",
        "fastapi",
        "bookmarks_converter",
        "transformers",
        "torchaudio",
        "torch",
        "aiohttp",
        "bs4",
        "dictknife",
        "libtorch",
        "torchvision",
        "anyio",
        "re"
        
    ],
}

setup(name = "unpacker", executables = [exe],options = {"build_exe": build_exe_options})




