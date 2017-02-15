from django.conf.urls  import url
from . import views
from django.contrib import admin

admin.autodiscover()


urlpatterns = [
    url(r'^login', views.login, name='login'),
    url(r'^logout', views.logout, name='logout'),
    url(r'^register', views.register, name='register'),
    url(r'^captcha',views.captcha,name='captcha'),
    url(r'^fgPasswd',views.fgPasswd,name='fgPasswd'),
    url(r'active=(?P<ciphertext>.+)',views.active_user,name='ciphertext'),
    url(r'^getLoginStatus',views.getLoginStatus,name='getLoginStatus'),
    url(r'^getUserInfo',views.getUserInfo,name='getUserInfo'),
    url(r'^editUsername',views.editUsername,name='editUsername'),
    url(r'^editUserMail',views.editUsername,name='editUsername'),
    url(r'^editUserAcceptPost ',views.editUserAcceptPost ,name='editUserAcceptPost '),
    url(r'^getWatchList ',views.getWatchList ,name='getWatchList '),
    url(r'^addWatchTag',views.addWatchTag,name='addWatchTag'),
    url(r'^delWatchTag ',views.delWatchTag ,name='delWatchTag '),
    url(r'.*',views.login,name='login'),

]