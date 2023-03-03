import os
import venv
import sys

def main():
    #仮想環境を作成する
    if(os.path.exists("/tmp/venv")):
        sys.exit(0)

    venv.create("/tmp/venv")
        


if __name__ == "__main__":
    main()