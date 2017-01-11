from django.conf.urls import url,include
<<<<<<< HEAD
from . import views
=======
from api import views
>>>>>>> eee6113b95b6f94b795bbd3ec39a0625545043ad

urlpatterns = [
    url(r'getHotWords/',views.getHotWords,name='getHotWords'),
    url(r'getHotNews/',views.getHotNews,name='getHotNews'),
    url(r'getHotTopics',views.getHotTopics,name='getHotTopics'),
    url(r'alterUserUrl',views.alterUserUrl,name='alterUserUrl'),
    url(r'alterUsersTopic',views.alterUsersTopic,name='alterUsersTopic'),
    url(r'alterUsersWord',views.alterUsersWord,name='alterUsersWord'),
    url(r'getUserInfo',views.getUserInfo,name='getUserInfo'),
    url(r'editUserInfo',views.editUserInfo,name='editUserInfo'),
<<<<<<< HEAD
    url(r'getNewsPage',views.getNewsPage,name='getNesPage'),
    url(r'getGraph',views.getGraph,name='getGraph'),
    url(r'postUserClick',views.postUserClick,name='postUserClick'),
    url(r'search',views.search,name='search'),
=======

>>>>>>> eee6113b95b6f94b795bbd3ec39a0625545043ad


]