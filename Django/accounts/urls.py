from django.conf.urls  import url
from accounts import views
from django.contrib import admin

admin.autodiscover()


urlpatterns = [
    url(r'^login', views.login, name='login'),
    url(r'^logout', views.logout, name='logout'),
    url(r'^register', views.register, name='register'),
    url(r'^captcha',views.captcha,name='captcha'),
    url(r'^fgPasswd',views.fgPasswd,name='fgPasswd'),
    url(r'active=(?P<ciphertext>.+)',views.active_user,name='ciphertext'),
    url(r'.*',views.login,name='login'),

]