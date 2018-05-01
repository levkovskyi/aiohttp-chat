import aiohttp_jinja2
from aiohttp_session import get_session
from aiohttp import web, WSMsgType


from chat.models import Message


class ChatList(web.View):
    @aiohttp_jinja2.template('chat/index.html')
    async def get(self):
        message = Message(self.request.app.db)
        messages = await message.get_messages()
        return {'messages': messages}
