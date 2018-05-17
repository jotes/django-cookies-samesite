import django
from django.conf.urls import url

import views

urlpatterns = [
    url('^cookies-test/$', views.cookies_test, name='cookie-test')
]
