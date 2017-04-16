from werkzeug.contrib.cache import MemcachedCache, SimpleCache
from flask import Flask

app = Flask(__name__, instance_relative_config=True)
#for production, use a real MemcacherCache service
# CACHE = MemcachedCache(['127.0.0.1:11211'])

# for dev, use SimpleCache
CACHE = SimpleCache()
