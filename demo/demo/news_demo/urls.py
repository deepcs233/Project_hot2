from django.conf.urls import url,include
from news_demo import views
urlpatterns=[
    url(r'^news',views.news),
    url(r'^postnews',views.postnews),
    ]
