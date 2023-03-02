import os
import venv
import sys

def main():
    #仮想環境を作成する
    if(os.path.exists("./venv")):
        sys.exit(0)

    venv.create("./venv")
        


if __name__ == "__main__":
    main()