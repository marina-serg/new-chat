from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('', consumers.JoinAndLeave.as_asgi()),
    path('ws/search_users/groups/<uuid:uuid>/', consumers.UserSearchConsumer.as_asgi()),
    path('ws/search_users/groups/<uuid:uuid>/invite/', consumers.UserSearchConsumer.as_asgi()),
    path('groups/<uuid:uuid>/', consumers.GroupConsumer.as_asgi()),
    path('groups/<uuid:uuid>/invite/', consumers.GroupConsumer.as_asgi()),

]
