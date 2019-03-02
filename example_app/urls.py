from django.conf.urls import include, url
from django.contrib import admin
from chatterbot.ext.django_chatterbot import urls as chatterbot_urls
from example_app.views import ChatterBotAppView,train_request


urlpatterns = [
    url(r'^$', ChatterBotAppView.as_view(), name='main'),
    url(r'^admin/', include(admin.site.urls), name='admin'),
    url(r'^chatterbot/', include('chatterbot.ext.django_chatterbot.urls', namespace='chatterbot')),
    url(r'^trainme/',train_request,name='training')
]