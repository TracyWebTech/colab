#!/usr/bin/env python
# encoding: utf-8

from django.core.urlresolvers import NoReverseMatch
from django.contrib.syndication.views import Feed
from django.utils.translation import ugettext as _

from haystack.query import SearchQuerySet

from super_archives.models import Thread, Message


class LatestThreadsFeeds(Feed):
    title = _(u'Latest Discussions')
    link = '/rss/threads/latest/'

    def items(self):
        return Thread.objects.all()[:20]

    def item_link(self, item):
        return item.latest_message.url

    def item_title(self, item):
        title = '[' + item.mailinglist.name + '] '
        title += item.latest_message.subject_clean
        return title

    def item_description(self, item):
        return item.latest_message.body


class HottestThreadsFeeds(Feed):
    title = _(u'Discussions Most Relevance')
    link = '/rss/threads/hottest/'

    def items(self):
        return Thread.highest_score.all()[:20]

    def item_link(self, item):
        return item.latest_message.url

    def item_title(self, item):
        title = '[' + item.mailinglist.name + '] '
        title += item.latest_message.subject_clean
        return title

    def item_description(self, item):
        return item.latest_message.body


class LatestColabFeeds(Feed):
    title = _(u'Latest collaborations')
    link = '/rss/colab/latest/'

    def items(self):
        items = SearchQuerySet().order_by('-modified', '-created')[:20]
        return items

    def item_title(self, item):
        type_ = item.type + ': '
        mailinglist = item.tag

        if mailinglist:
            prefix = type_ + mailinglist + ' - '
        else:
            prefix = type_

        return prefix + item.title

    def item_description(self, item):
        return item.latest_description

    def item_link(self, item):
        return item.url


class LatestUserThreadsFeeds(Feed):
    title = _(u'Latest User Discussions')
    link = '/rss/threads/latest/user/'

    def __call__(self, request, *args, **kwargs):
        self.username = kwargs.get('username')

        return super(LatestUserThreadsFeeds, self).__call__(
            request, *args, **kwargs
        )

    def items(self):
        return Message.objects.filter(
            from_address__user__username=self.username
        )[:20]

    def item_link(self, item):
        try:
            return item.thread.get_absolute_url()
        except NoReverseMatch:
            return ''

    def item_title(self, item):
        title = '[' + item.mailinglist.name + '] '
        title += item.subject_clean
        return title

    def item_description(self, item):
        return item.body


class LatestUserContributionsFeeds(Feed):
    title = _(u'Latest User Contributions')
    link = '/rss/colab/latest/user/'

    def __call__(self, request, *args, **kwargs):
        self.username = kwargs.get('username')

        return super(LatestUserContributionsFeeds, self).__call__(
            request, *args, **kwargs
        )

    def items(self):
        return SearchQuerySet().filter(
            collaborators__contains=self.username,
        )[:20]

    def item_link(self, item):
        return item.url

    def item_title(self, item):
        title = '[' + item.title + '] '
        return title

    def item_description(self, item):
        descr = item.description
        return descr if len(descr) <= 800 else descr[:797] + '...'
