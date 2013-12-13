# -*- coding: utf-8 -*-

import pygal

from colab.utils.pygal_style import CustomLightStyle


def render_pie_chart(count_dict, style=CustomLightStyle, width=None,
                     height=None, no_data_text='', value_font_size=15,
                     explicit_size=True):

    pie_chart = pygal.Pie(style=style, width=width, height=height,
                          no_data_text=no_data_text,
                          value_font_size=value_font_size,
                          explicit_size=explicit_size)

    for count in tuple(count_dict.items()):
        pie_chart.add(count[0], count[1])

    return pie_chart.make_instance(
        overrides={'disable_xml_declaration': True}
    ).render(is_unicode=True)
