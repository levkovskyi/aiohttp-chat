from aiohttp import web
from aiohttp_session import get_session

from auth.models import User


@web.middleware
async def request_user_middleware(request, handler):
    request.session = await get_session(request)
    request.user = None

    user_id = request.session.get('user')
    if user_id:
        request.user = await User(request.app.db, {'id': request.session.get('user')}).get_user()
    return await handler(request)
