import hashlib

import aiohttp_jinja2
import jinja2
from aiohttp import web
from aiohttp_session import session_middleware
from aiohttp_session.cookie_storage import EncryptedCookieStorage

from core.middlewares import request_user_middleware
from core.ws import ws_shutdown
from core.db import init_db, close_db
from urls import routes, static_routes
from settings import log
import settings

middle = [
    session_middleware(EncryptedCookieStorage(hashlib.sha256(bytes(settings.SECRET_KEY, 'utf-8')).digest())),
    request_user_middleware
]

app = web.Application(middlewares=middle)

aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('templates'))

# route part
app.router.add_routes(routes)
app['static_root_url'] = static_routes.path
# end route part

# db connect
app.on_startup.append(init_db)
app.on_cleanup.append(close_db)
# end db connect

app.on_cleanup.append(ws_shutdown)
app['websockets'] = []

log.debug('start server')
web.run_app(app, host='localhost', port=8080)
log.debug('Stop server end')
