import aiohttp_jinja2
from aiohttp import web, WSMsgType

from chat.models import Message
from core.decorators import login_required
from settings import log


class ChatList(web.View):

    @login_required
    @aiohttp_jinja2.template('chat/index.html')
    async def get(self):
        message = Message(self.request.app.db)
        messages = await message.get_messages()
        return {'messages': messages}


class WebSocket(web.View):

    @login_required
    async def get(self):
        ws = web.WebSocketResponse()
        await ws.prepare(self.request)

        user = self.request.user
        login = user.get('login')

        for _ws in self.request.app['websockets']:
            await _ws.send_str('%s joined' % login)
        self.request.app['websockets'].append(ws)

        async for msg in ws:
            if msg.type == WSMsgType.TEXT:
                if msg.data == 'close':
                    await ws.close()
                else:
                    message = Message(self.request.app.db)
                    result = await message.save(user=login, msg=msg.data)
                    log.debug(result)
                    for _ws in self.request.app['websockets']:
                        await _ws.send_str('{"user": "%s", "msg": "%s"}' % (login, msg.data))
            elif msg.type == WSMsgType.ERROR:
                log.debug('ws connection closed with exception %s' % ws.exception())

        self.request.app['websockets'].remove(ws)
        for _ws in self.request.app['websockets']:
            await _ws.send_str('%s disconected' % login)
        log.debug('websocket connection closed')

        return ws
