"""douban_client URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index,name='index'),
    url(r'^login', views.login,name='login'),
    url(r'^register', views.register,name='register'),
    url(r'^film/(?P<ntype>\d+)/(?P<npage>\d+)', views.films, name='film'),
    url(r'^film/search', views.search, name='search'),
    #url(r'^detail/(?P<film_id>\d+)$', views.detail, name='detail'),
    url(r'.*', views.notexist, name='404'),
]