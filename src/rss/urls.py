from django.conf.urls import patterns, url
import feeds

urlpatterns = patterns('',
    url(r'threads/latest/$', feeds.LatestThreadsFeeds(), name='rss_latest_threads'),
    url(r'colab/latest/$', feeds.LatestColabFeeds(), name='rss_latest_colab'),
    url(r'threads/hottest/$', feeds.HottestThreadsFeeds(), name='rss_hottest_threads'),
    url(
        r'threads/latest/(?P<username>[\w+.-]+)/$',
        feeds.LatestUserThreadsFeeds(),
        name='rss_user_latest_threads'
    ),
    url(
        r'colab/latest/(?P<username>[\w+.-]+)/$',
        feeds.LatestUserContributionsFeeds(),
        name='rss_user_latest_contributions'
    ),
)

