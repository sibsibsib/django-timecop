from django.contrib import admin

from .models import Timeline, TimeSpan


class InlineTimeSpanAdmin(admin.TabularInline):
    model = TimeSpan
    extra = 0


class TimelineAdmin(admin.ModelAdmin):
    inlines = (InlineTimeSpanAdmin, )

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


admin.site.register(Timeline, TimelineAdmin)
