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
from .utils import CustomLightStyle


def index(request):
    """Index page view"""


    latest_threads = Thread.objects.all()[:6]
    hottest_threads = Thread.highest_score.from_haystack()[:6]

    pie_chart_dict = cache.get('home_chart')
    if pie_chart_dict is None:
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

        PIE_WIDTH = 500
        PIE_HEIGHT = 350
        pie_chart = pygal.Pie(
            style=CustomLightStyle, width=PIE_WIDTH, height=PIE_HEIGHT,
            no_data_text=_(u'No data found'), value_font_size=15
        )
        for count in tuple(count_types.items()):
            pie_chart.add(count[0], count[1])

        pie_chart_dict = dict(
            render=pie_chart.make_instance(
                overrides={'disable_xml_declaration': True}
            ).render(is_unicode=True),
            width=PIE_WIDTH,
            height=PIE_HEIGHT,
        )
        cache.set('home_chart', pie_chart_dict)

    context = {
        'hottest_threads': hottest_threads[:6],
        'latest_threads': latest_threads,
        'pie_chart': pie_chart_dict,
        'latest_results': SearchQuerySet().all().order_by(
            '-modified', '-created'
        )[:6],
    }
    return render(request, 'home.html', context)
