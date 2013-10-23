from django.template import Library

from timecop.models import Timeline


register = Library()


@register.simple_tag
def timelines_to_json(timelines):
    return  Timeline.timelines_to_json(timelines)
