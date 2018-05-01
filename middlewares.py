from aiohttp import web
from aiohttp_session import get_session


@web.middleware
async def authorize(request, handler):
    def check_path(path):
        result = True
        for r in ['/login', '/static/', '/sign-in', '/sign-out', '/_debugtoolbar/']:
            if path.startswith(r):
                result = False
                break
        return result

    session = await get_session(request)

    if not session.get("user") and check_path(request.path):
        url = request.app.router['login'].url_for()
        raise web.HTTPFound(url)
    return await handler(request)
