from auth.urls import routes as auth_routes
from chat.urls import routes as chat_routes


routes = (
    * auth_routes,
    * chat_routes,
)
