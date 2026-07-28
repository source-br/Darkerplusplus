from app import HammerfyApp
import sys
import os

if __name__ == "__main__":
    app = HammerfyApp(sys.argv)
    ret = app.exec()
    os._exit(ret)