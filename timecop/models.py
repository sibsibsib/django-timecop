import json

from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.utils.safestring import mark_safe
from django.utils.timezone import now
from django.utils.functional import lazy

from .conf import get_timeline_model_path, get_timespan_model


def get_sequence(slug):
    current_time = now()
    TimeSpan = get_timespan_model()
    spans = TimeSpan.objects.order_by('-start', '-end', '-id').filter(timeline__slug=slug)

    current_span = None
    next_span = None

    for span in spans:
        if span.start <= current_time < span.end:
            current_span = span
            break

        if span.start > current_time:
            next_span = span

    return {
        'current': current_span,
        'next': next_span,
        'all_spans':  list(reversed(spans))
    }

get_sequence_lazy = lazy(get_sequence, dict)


class AbstractTimeline(models.Model):

    slug = models.SlugField(u'slug', default=None, max_length=255, unique=True,
        db_index=True, help_text=u'a unique identifier')

    JSON_ENCODER = DjangoJSONEncoder

    class Meta:
        abstract = True

    def __unicode__(self):
        return self.slug

    @classmethod
    def timelines_to_json(cls, timelines, indent=None):
        return mark_safe(json.dumps(map(cls.to_dict, timelines), cls=cls.JSON_ENCODER, indent=indent))

    def to_dict(self):
        return {
            'id': self.id,
            'slug': self.slug,
            'sequence': [span.to_dict() for span in self.get_spans()],
        }

    def to_json(self, indent=None):
        return mark_safe(json.dumps(self.to_dict(), cls=DjangoJSONEncoder, indent=indent))

    def get_spans(self):
        return self.spans.all()


class AbstractTimeSpan(models.Model):

    timeline = models.ForeignKey(get_timeline_model_path(), default=None, related_name='spans')

    slug = models.SlugField(u'slug', default=None, max_length=255, unique=True,
        help_text=u'a unique identifier')
    start = models.DateTimeField(u'start', default=None,
        help_text='inclusive')
    end = models.DateTimeField(u'end', default=None,
        help_text='exclusive')

    class Meta:
        abstract = True
        ordering = ('start', 'end', 'id',)

    def __unicode__(self):
        return self.slug

    @property
    def timedelta(self):
        return self.end - self.start

    def to_dict(self):
        return {
            'id': self.id,
            'slug': self.slug,
            'start': self.start,
            'end': self.end,
        }
