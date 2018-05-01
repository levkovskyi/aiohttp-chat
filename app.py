from aiohttp_session import session_middleware
from aiohttp_session.cookie_storage import EncryptedCookieStorage
from aiohttp import web
import aiohttp_jinja2
import jinja2

import hashlib
from motor import motor_asyncio as ma

from middlewares import authorize
from routes import routes
from utils import ws_shutdown
from settings import log
import settings


middle = [
    session_middleware(EncryptedCookieStorage(hashlib.sha256(bytes(settings.SECRET_KEY, 'utf-8')).digest())),
    authorize
]

app = web.Application(middlewares=middle)

aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('templates'))

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

app.on_cleanup.append(ws_shutdown)
app['websockets'] = []

log.debug('start server')
web.run_app(app)
log.debug('Stop server end')
