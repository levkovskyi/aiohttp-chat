from auth import views


routes = (
    dict(method='*', path='/login', handler=views.Login, name='login'),
    dict(method='*', path='/sign-in', handler=views.SignIn, name='sign_in'),
    dict(method='GET', path='/logout', handler=views.Logout, name='logout'),
)
