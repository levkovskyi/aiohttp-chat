async def ws_shutdown(app):
    for ws in app['websockets']:
        await ws.close(code=1001, message='Server shutdown')
