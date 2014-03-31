from django.contrib import admin

from .conf import get_timespan_model


class BaseTimeSpanAdmin(admin.TabularInline):

    model = get_timespan_model()
    extra = 0


class BaseTimelineAdmin(admin.ModelAdmin):

    class Media:
        css = {
            'all': ('components/timeline/timeline.css',),
        }
        js = (
            'components/jquery/jquery-2.0.3.min.js',
            'components/underscore/underscore-min.js',
            'components/backbone/backbone.js',
            'components/backbone.stickit/backbone.stickit.js',
            'components/timeline/timeline-min.js',
            'components/moment/moment.min.js',

            'js/timecop.js',
        )
