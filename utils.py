import json


def error_json(message):
    return json.dumps({'error': message})


async def ws_shutdown(app):
    for ws in app['websockets']:
        await ws.close(code=1001, message='Server shutdown')
