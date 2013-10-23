import json

from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.utils.safestring import mark_safe


class Timeline(models.Model):

    slug = models.SlugField(u'slug', default=None, max_length=255, unique=True,
        help_text=u'a unique identifier')

    JSON_ENCODER = DjangoJSONEncoder

    def __unicode__(self):
        return self.slug

    @classmethod
    def timelines_to_json(cls, timelines, indent=None):
        return mark_safe(json.dumps(map(cls.to_dict, timelines), cls=cls.JSON_ENCODER, indent=indent))

    def to_dict(self):
        return {
            'id': self.id,
            'slug': self.slug,
            'sequence': map(TimeSpan.to_dict, self.spans.all()),
        }

    def to_json(self, indent=None):
        return mark_safe(json.dumps(self.to_dict(), cls=DjangoJSONEncoder, indent=indent))


class TimeSpan(models.Model):

    timeline = models.ForeignKey(Timeline, default=None, related_name='spans')

    slug = models.SlugField(u'slug', default=None, max_length=255, unique=True,
        help_text=u'a unique identifier')
    start = models.DateTimeField(u'start', default=None,
        help_text='inclusive')
    end = models.DateTimeField(u'end', default=None,
        help_text='exclusive')

    class Meta:
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
