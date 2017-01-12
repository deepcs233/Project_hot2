from django.conf.urls import url,include

from . import views

from api import views


urlpatterns = [
    url(r'getHotWords/',views.getHotWords,name='getHotWords'),
    url(r'getHotNews/',views.getHotNews,name='getHotNews'),
    url(r'getHotTopics',views.getHotTopics,name='getHotTopics'),
    url(r'alterUserUrl',views.alterUserUrl,name='alterUserUrl'),
    url(r'alterUsersTopic',views.alterUsersTopic,name='alterUsersTopic'),
    url(r'alterUsersWord',views.alterUsersWord,name='alterUsersWord'),
    url(r'getUserInfo',views.getUserInfo,name='getUserInfo'),
    url(r'editUserInfo',views.editUserInfo,name='editUserInfo'),
    url(r'getNewsPage',views.getNewsPage,name='getNesPage'),
    url(r'getGraph',views.getGraph,name='getGraph'),
    url(r'postUserClick',views.postUserClick,name='postUserClick'),
    url(r'search',views.search,name='search'),



]
