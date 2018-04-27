from aiohttp_session import session_middleware
from aiohttp_session.cookie_storage import EncryptedCookieStorage
from aiohttp import web

import hashlib
from motor import motor_asyncio as ma

import settings
from settings import log
from routes import routes


middle = [
    session_middleware(EncryptedCookieStorage(hashlib.sha256(bytes(settings.SECRET_KEY, 'utf-8')).digest())),
]

app = web.Application(middlewares=middle)

# route part
for route in routes:
    app.router.add_route(route[0], route[1], route[2], name=route[3])
app['static_root_url'] = '/static'
app.router.add_static('/static', 'static', name='static')
# end route part

# db connect
app.client = ma.AsyncIOMotorClient(settings.MONGO_HOST)
app.db = app.client[settings.MONGO_DB_NAME]
# end db connect

log.debug('start server')
web.run_app(app)
log.debug('Stop server end')
