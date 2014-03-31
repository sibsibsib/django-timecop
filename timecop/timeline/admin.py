from django.contrib import admin

from timecop.admin import BaseTimelineAdmin

.models import TimeSpan, Timeline


class InlineTimeSpanAdmin(BaseTimeSpanInline):
    pass


class TimelineAdmin(BaseTimelineAdmin):
    inlines = (InlineTimeSpanAdmin,)


admin.site.register(Timeline, TimelineAdmin)
