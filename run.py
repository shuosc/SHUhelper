from gevent import monkey
monkey.patch_all(thread=False)
from UHE.app import create_app
# from UHE.extensions import celery 

app = create_app()
print('app start')