from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

import rest.routes

urlpatterns = patterns('',

    url(r'^update', 'rest.routes.update'),

)
