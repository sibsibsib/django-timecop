from django.template import Library

from timecop.conf import get_timeline_model

register = Library()


@register.simple_tag
def timelines_to_json(timelines):
    Timeline = get_timeline_model()
    return Timeline.timelines_to_json(timelines)
