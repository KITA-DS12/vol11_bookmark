import subprocess
import sys

def main():
    o = subprocess.check_output(
        args="pip install fastapi uvicorn python-multipart bookmarks-converter datasets evaluate transformers[sentencepiece] torchaudio --extra-index-url https://download.pytorch.org/whl/cpu torch torchvision aiohttp Beautifulsoup4 pyinstaller dictknife",
        shell=True
    )
    print(o)

if __name__ == "__main__":
    main()
    