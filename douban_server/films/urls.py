from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.films),
    url(r'^/(\d+)/(\d+)$', views.films),
]
