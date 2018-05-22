from aiohttp import web
from aiohttp_session import get_session
from bson.objectid import ObjectId

from auth.models import User


@web.middleware
async def request_user_middleware(request, handler):
    request.session = await get_session(request)
    request.user = None

    user_id = request.session.get('user')
    if user_id:
        request.user = await User.find_one({'id': ObjectId(user_id)})
    return await handler(request)
