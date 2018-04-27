from auth.views import Login, SignIn, SignOut


routes = [
    ('*',   '/login',   Login,     'login'),
    ('*',   '/sign-in',  SignIn,    'sign_in'),
    ('*',   '/logout', SignOut,   'logout'),
]
