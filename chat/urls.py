from chat import views


routes = (
    dict(method='GET', path='/', handler=views.ChatList, name='main'),
    dict(method='GET', path='/ws', handler=views.WebSocket, name='chat'),
)
