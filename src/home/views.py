# -*- coding: utf-8 -*-

import pygal

from collections import OrderedDict

from django.core.cache import cache
from django.shortcuts import render
from django.utils.translation import ugettext as _

from search.utils import trans
from haystack.query import SearchQuerySet

from proxy.models import WikiCollabCount, TicketCollabCount
from super_archives.models import Thread
from colab.utils.pygal_render import render_pie_chart


def index(request):
    """Index page view"""


    latest_threads = Thread.objects.all()[:6]
    hottest_threads = Thread.highest_score.from_haystack()[:6]

    home_chart = cache.get('home_chart')
    if home_chart is None:
        count_types = OrderedDict()
        for type in ['thread', 'changeset', 'attachment']:
            count_types[trans(type)] = SearchQuerySet().filter(
                type=type,
            ).count()

        count_types[trans('ticket')] = sum([
            ticket.count for ticket in TicketCollabCount.objects.all()
        ])

        count_types[trans('wiki')] = sum([
            wiki.count for wiki in WikiCollabCount.objects.all()
        ])

        home_chart = render_pie_chart(count_types, width=500, height=350,
            no_data_text=_(u'No data found')
        )
        cache.set('home_chart', home_chart)

    context = {
        'hottest_threads': hottest_threads[:6],
        'latest_threads': latest_threads,
        'home_chart': home_chart,
        'latest_results': SearchQuerySet().all().order_by(
            '-modified', '-created'
        )[:6],
    }
    return render(request, 'home.html', context)
