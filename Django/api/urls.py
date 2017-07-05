from django.conf.urls import url,include

from . import views



urlpatterns = [
    url(r'getHotWords/',views.getHotWords,name='getHotWords'),
    url(r'getNewsPage',views.getNewsPage,name='getNewsPage'),
    url(r'getGraph',views.getGraph,name='getGraph'),
    url(r'postUserClick',views.postUserClick,name='postUserClick'),
    url(r'getSearchGraph',views.getSearchGraph,name='getSearchGraph'),
    url(r'getSearchNews',views.getSearchNews,name='getSearchNews'),
    url(r'getHotWords',views.getHotWords,name='getHotWords'),
    url(r'clickNews',views.clickNews,name='clickNews'),
    url(r'newstrail',views.newstrail,name='newstrail'),
    url(r'geodata',views.geodata,name='geodata'),
]
