import json

from aiohttp import web


def error_json(message):
    return json.dumps({'error': message})


async def ws_shutdown(app):
    for ws in app['websockets']:
        await ws.close(code=1001, message='Server shutdown')


def redirect(request, router_name, *, permanent=False, **kwargs):
    """ Redirect to given URL name """
    url = request.app.router[router_name].url_for(**kwargs)
    if permanent:
        raise web.HTTPMovedPermanently(url)
    raise web.HTTPFound(url)
