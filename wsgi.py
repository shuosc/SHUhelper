from gevent import monkey
monkey.patch_all(thread=False)
from UHE.app import create_app
app = create_app()
if __name__ == "__main__":
   app.run()