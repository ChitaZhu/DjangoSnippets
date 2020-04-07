#!/usr/bin/env python
# encoding: utf-8

"""
@author: xulei
@contact: robin.xulei@gmail.com
@software: PyCharm
@file: urls
@time: 2019-07-31 10:59
"""
from django.conf.urls import url
from news.views import ReporterViewSet, ArticleViewSet

urlpatterns = [
    url('^reporter$', ReporterViewSet.as_view(), name='reporter'),
    url('^article', ArticleViewSet.as_view(), name='article'),
]