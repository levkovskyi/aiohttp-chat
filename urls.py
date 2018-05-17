from aiohttp import web

from auth.urls import routes as auth_routes
from chat.urls import routes as chat_routes
import settings


static_routes = web.static('/static', settings.STATIC_DIR, name='static')

routes = (
    * auth_routes,
    * chat_routes,
    static_routes
)
