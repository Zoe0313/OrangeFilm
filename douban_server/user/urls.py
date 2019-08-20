from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$',views.users, name='users'),
    #/v1/users/liuxiaoxia
    url(r'^/(?P<username>[\w]{3,11})$',views.users, name='user'),
    #/v1/users/liuxiaoxia/avatar
    url(r'^/(?P<username>[\w]{3,11})/avatar$',views.user_avatar, name='user_avatar'),
]