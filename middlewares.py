from aiohttp import web
from aiohttp_session import get_session


@web.middleware
async def authorize(request, handler):
    def check_path(path):
        result = True
        for r in ['/login', '/static/', '/sign-in', '/sign-out', '/_debugtoolbar/']:
            if path.startswith(r):
                result = False
        return result

    session = await get_session(request)
    if session.get("user"):
        return await handler(request)
    elif check_path(request.path):
        url = request.app.router['login'].url_for()
        raise web.HTTPFound(url)
    else:
        return await handler(request)
