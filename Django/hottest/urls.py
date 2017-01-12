from django.conf.urls import url,include


from . import views
from django.contrib import admin

admin.autodiscover()


urlpatterns = [
        url(r'.*', views.index, name='guide'),
        url(r'index',views.index,name='index'),
        url(r'guide',views.guide,name='guide'),


        ]