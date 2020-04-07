#!/usr/bin/env python
# encoding: utf-8

from django.conf.urls import url
from file.views import FileViewSet, file_download

urlpatterns = [
    url('^upload$', FileViewSet.as_view(), name='file'),
    url('^download$', file_download.as_view(), name='file')
]