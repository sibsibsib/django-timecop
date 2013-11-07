django-timecop
==============

Timecop is a reusable Django app for managing events on timelines. Create and
edit timelines with events from the django admin.


Installation
------------

Add `timecop` to `INSTALLED_APPS` and then run `syncdb`.


Usage
-----

Timecop adds two models: `Timeline` and `TimeSpan`. Spans attach to timelines.

Your application can then foreign key to these models and retrieve them through
the usual Django ORM queries.


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

