from auth.views import Login, SignIn, Logout
from chat.views import ChatList, WebSocket


routes = [
    ('GET', '/', ChatList, 'main'),
    ('GET', '/ws', WebSocket, 'chat'),
    ('*',   '/login',   Login,     'login'),
    ('*',   '/sign-in',  SignIn,    'sign_in'),
    ('*',   '/logout', Logout,   'logout'),
]
