from aiohttp import web

from chat import views


routes = (
    web.view('/', views.ChatList, name='main'),
    web.view('/ws', views.WebSocket, name='chat'),
)
