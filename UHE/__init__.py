__version__ = '1.0'
from UHE.app import create_app

if __name__ == "__main__":
    app = create_app()
    app.run()
    print('start')