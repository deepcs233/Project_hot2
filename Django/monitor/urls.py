from django.conf.urls import url
from . import views

urlpatterns = [
        url(r'addWatchUrl',views.addWatchUrl ,name='addWatchUrl'),
        url(r'delWatchUrl',views.delWatchUrl ,name='delWatchUrl'),
        url(r'getWatchUrl',views.getWatchUrl,name='getWatchUrl'),
        url(r'getWatchThing',views.getWatchThing,name='getWatchThing'),
        ]

