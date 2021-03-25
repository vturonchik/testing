# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.TopicListView.as_view(), name='home'),
    url(r'^register/$', views.RegisterFormView.as_view()),
    url('', include('django.contrib.auth.urls')),
    url(r'^(?P<topic_id>\d+)/(?P<pk>\d+)/$', views.TestDetailView.as_view(), name='test-details'),
    url(r'^results/$', views.ResultsTemplateView.as_view(), name='results'),
]