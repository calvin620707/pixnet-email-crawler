from django.conf.urls import url
from crawlers import views

urlpatterns = [
    url(r'^$', views.index, name='index')
]
