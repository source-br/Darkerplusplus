from app import HammerfyApp
import sys

if __name__ == "__main__":
    app = HammerfyApp(sys.argv)
    sys.exit(app.exec())