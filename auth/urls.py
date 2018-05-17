from aiohttp import web

from auth import views


routes = (
    web.view('/login', views.Login, name='login'),
    web.view('/sign-in', views.SignIn, name='sign_in'),
    web.view('/logout', views.Logout, name='logout'),
)
