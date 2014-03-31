from django.conf import settings
from django.utils.module_loading import import_by_path


def get_timeline_model_path():
    path = getattr(settings, 'TIMECOP_TIMELINE_MODEL', 'timecop.timeline.Timeline')
    return path.replace('models.', '')


def get_timeline_model():
    return import_by_path(getattr(settings, 'TIMECOP_TIMELINE_MODEL', 'timecop.timeline.models.Timeline'))


def get_timespan_model():
    return import_by_path(getattr(settings, 'TIMECOP_TIMESPAN_MODEL', 'timecop.timeline.models.TimeSpan'))

