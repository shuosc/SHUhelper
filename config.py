from werkzeug.contrib.cache import MemcachedCache, SimpleCache

#for production, use a real MemcacherCache service
# CACHE = MemcachedCache(['127.0.0.1:11211'])

# for dev, use SimpleCache
CACHE = SimpleCache()
