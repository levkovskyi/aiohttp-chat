from auth.views import Login, SignIn, Logout
from chat.views import ChatList


routes = [
    ('GET', '/', ChatList, 'main'),
    ('*',   '/login',   Login,     'login'),
    ('*',   '/sign-in',  SignIn,    'sign_in'),
    ('*',   '/logout', Logout,   'logout'),
]
