from django.conf.urls.defaults import *

# app imports
from alibrary.views import *

urlpatterns = patterns('',

    url(r'^$', MediaListView.as_view(), name='alibrary-media-list'),
    url(r'^(?P<pk>\d+)-(?P<slug>[-\w]+)/$', MediaDetailView.as_view(), name='alibrary-media-detail'),
    url(r'^(?P<pk>\d+)/edit/$', MediaEditView.as_view(), name='alibrary-media-edit'),
    
    url(r'^(?P<uuid>[-\w]+)/stream.mp3$', 'alibrary.views.stream_html5', name='alibrary-media-stream_html5'),
    url(r'^(?P<uuid>[-\w]+)/stream.(?P<bitrate>\d+).(?P<format>[-\w]+)$', 'alibrary.views.encode', name='alibrary-media-encode'),
    url(r'^(?P<uuid>[-\w]+)/waveform.png$', 'alibrary.views.waveform', name='alibrary-media-waveform'),
    #url(r'^tracks/(?P<uuid>[-\w]+)/stream_html5/base.mp3$', 'alibrary.views.stream_html5', name='alibrary-media-stream_html5'),
    #url(r'^tracks/(?P<uuid>[-\w]+)/waveform/$', 'alibrary.views.waveform', name='alibrary-media-waveform'),
    #url(r'^encode/(?P<uuid>[-\w]+)/stream.(?P<bitrate>\d+).(?P<format>[-\w]+)$', 'alibrary.views.encode', name='alibrary-media-encode'),

)