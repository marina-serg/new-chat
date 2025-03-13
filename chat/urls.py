from django.urls import path

from . import views

urlpatterns = [
    path('groups/<uuid:uuid>/invite/', views.group_chat_view, name='invite_user'),
    path('group/<uuid:group_uuid>/clear_chat/', views.clear_chat, name='clear_chat'),
    path("groups/<uuid:uuid>/", views.group_chat_view, name="group"),
    path("", views.home_view, name="home"),

]
