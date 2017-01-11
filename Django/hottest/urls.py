from django.conf.urls import url,include


from hottest import views
from django.contrib import admin

admin.autodiscover()


urlpatterns = [
        url(r'index',views.index,name='index'),
        url(r'guide',views.guide,name='guide'),
        url(r'.*', views.guide, name='guide'),

        ]