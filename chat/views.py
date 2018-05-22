import aiohttp_jinja2
from aiohttp import web, WSMsgType
from marshmallow.exceptions import ValidationError

from chat.models import Message
from chat import schemas
from core.decorators import login_required
from core.db import include_references
from settings import log


class ChatList(web.View):
    @login_required
    @aiohttp_jinja2.template('chat/index.html')
    async def get(self):
        cursor = Message.find()
        messages = await cursor.to_list(100)
        await include_references(messages, ['user_id'])
        schema = schemas.MessageSchema()
        ms = schema.dump(obj=messages, many=True).data

        return {'messages': ms}


class WebSocket(web.View):
    @login_required
    async def get(self):
        ws = web.WebSocketResponse()
        await ws.prepare(self.request)

        user = self.request.user

        for _ws in self.request.app['websockets']:
            await _ws.send_str('%s joined' % user.login)
        self.request.app['websockets'].append(ws)

        async for msg in ws:
            if msg.type == WSMsgType.TEXT:
                if msg.data == 'close':
                    await ws.close()

                else:
                    try:
                        message = Message(message=msg.data, user_id=user)
                        await message.commit()
                    except ValidationError as e:
                        print(e)
                    for _ws in self.request.app['websockets']:
                        await _ws.send_str('{"user": "%s", "msg": "%s"}' % (user.login, msg.data))
            elif msg.type == WSMsgType.ERROR:
                log.debug('ws connection closed with exception %s' % ws.exception())

        self.request.app['websockets'].remove(ws)
        for _ws in self.request.app['websockets']:
            await _ws.send_str('%s disconected' % user.login)
        log.debug('websocket connection closed')

        return ws
