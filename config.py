from werkzeug.contrib.cache import MemcachedCache
from werkzeug.contrib.cache import SimpleCache

#for production, use a real MemcacherCache service
# CACHE = MemcachedCache(['127.0.0.1:11211'])

# for dev, use SimpleCache
CACHE = SimpleCache()