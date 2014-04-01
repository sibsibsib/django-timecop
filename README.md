django-timecop
==============

Timecop is a reusable Django app for managing events on timelines. Create and
edit timelines with events from the django admin.


Installation
------------

Add `timecop` to `INSTALLED_APPS`. If using the built-in timeline objects,
add  'timecop.timeline'.


Usage
-----

Timecop adds two models: `Timeline` and `TimeSpan`. Spans attach to timelines and
represent a block of time.

Your application can then foreign key to these models and retrieve them through
the usual Django ORM queries. Additionally, timecop provides a helper function
to get an entire sequence of spans for a given timeline:

    >>> from timecop.models import get_sequence
    >>> get_sequence('campaign')
    {
        'current': <TimeSpan: phase2>,
        'all_spans': [
            <TimeSpan: phase1>,
            <TimeSpan: phase2>,
            <TimeSpan: phase3>
        ],
        'next': <TimeSpan: phase3>
    }


### Custom models

To provide your own models for TimeSpan and Timeline, simply subclass AbstractTimeline
and AbstractTimespan and then update the following settings:


    TIMECOP_TIMELINE_MODEL = 'customapp.models.Timeline'
    TIMECOP_TIMESPAN_MODEL = 'customapp.models.TimeSpan'


The current model class for each can be retrieved by using the `get_timeline_model`
or `get_timespan_model` from `timecop.conf`.


### Custom admin

If using custom models, you'll need to extend the timecop admin base classes
`BaseTimeSpanAdmin`, `BaseTimelineAdmin` and templates in order to see the
timeline view in the admin.

*templates/admin/customapp/timeline/change_form.html:*

    {% extends "admin/timecop/timeline/change_form.html" %}


*templates/admin/customapp/timeline/change_list.html:*

    {% extends "admin/timecop/timeline/change_list.html" %}



Editing timelines
-----------------

Timecop's main benefit is providing a graphical overview of your timelines via
[chap-links timeline](http://almende.github.io/chap-links-library/timeline.html).


### List view:

<img src="https://raw.github.com/sibsibsib/django-timecop/master/docs/images/admin-timeline-changelist.png">

The list view provides a high-level overview of all timelines, as well as a
marker for the current time (shown in red).


### Change view:

<img src="https://raw.github.com/sibsibsib/django-timecop/master/docs/images/admin-timeline-changeform.png">

Change view provides interactive modification of time spans within a timeline.
Drag + drop to move or resize spans, or edit through the standard inputs.


Limitations
-----------

* When using the Django date picker shortcuts (ie calendar), the timeline
display will not update.

* When using 'add another' link in the change form, the new item is not inserted
into the timeline display. Clicking 'save and continue editing' will refresh
the display.

