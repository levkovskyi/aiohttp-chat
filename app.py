import hashlib

import aiohttp_jinja2
import jinja2
from aiohttp import web
from aiohttp_session import session_middleware
from aiohttp_session.cookie_storage import EncryptedCookieStorage
from motor import motor_asyncio as ma

import settings
from core.middlewares import request_user_middleware
from core.utils import ws_shutdown
from settings import log
from urls import routes

middle = [
    session_middleware(EncryptedCookieStorage(hashlib.sha256(bytes(settings.SECRET_KEY, 'utf-8')).digest())),
    request_user_middleware
]

app = web.Application(middlewares=middle)

aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('templates'))

# route part
for route in routes:
    app.router.add_route(**route)
app['static_root_url'] = '/static'
app.router.add_static('/static', settings.STATIC_DIR, name='static')
# end route part

# db connect
app.client = ma.AsyncIOMotorClient(settings.MONGO_HOST)
app.db = app.client[settings.MONGO_DB_NAME]
# end db connect

app.on_cleanup.append(ws_shutdown)
app['websockets'] = []

log.debug('start server')
web.run_app(app)
log.debug('Stop server end')
