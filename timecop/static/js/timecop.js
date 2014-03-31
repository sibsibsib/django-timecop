(function() {
    'use strict';

    var global = this;

    var $ = global.jQuery;
    var _ = global._;
    var Backbone = global.Backbone;
    var moment = global.moment;
    var links = global.links;

    var TimeCop = global.TimeCop = (global.TimeCop || {});


    TimeCop.parse_from_inlines = function(group_selector) {
        var $group = $(group_selector);

        var views = [];
        var collection = new Backbone.Collection();

        $group.find('.dynamic-spans').each(function(index, el) {

            var model = new Backbone.Model({
                index: index,
                ref_id: el.id,
                id: get_inline_field(el.id, 'id'),
                slug: get_inline_field(el.id, 'slug'),
                start_0: get_inline_field(el.id, 'start_0'),
                start_1: get_inline_field(el.id, 'start_1'),
                end_0: get_inline_field(el.id, 'end_0'),
                end_1: get_inline_field(el.id, 'end_1'),
                del: get_inline_field(el.id, 'DELETE')
            });

            collection.add(model);

            var view = new SpanView({
                el: el,
                model: model
            });

            views.push(view);
        });

        var timeline_view = new TimelineView({collection: collection, el:'#timeline'});
        timeline_view.render(); // TODO: move me
        views.push(timeline_view);

        return views;
    };


    function get_inline_field(inline_id, field_name) {
        var $el = $('#id_' + inline_id + '-' + field_name);
        return $el.is(':checkbox') ? $el.prop('checked') : $el.val();
    }


    function date_from_split_values(dateval, timeval) {
        return moment(dateval + 'T' + timeval);
    }


    // TODO: django date picker shortcuts (ie calendar, 'midnight') not triggering change event on input
    var SpanView = TimeCop.SpanView = Backbone.View.extend({});

    SpanView.prototype.initialize = function() {
        this.stickit(this.model, this.get_bindings());
    };

    SpanView.prototype.get_bindings = function() {
        var field = this.field_selector.bind(this);
        var bindings = {};

        bindings[field('id')] = 'id';
        bindings[field('slug')] = 'slug';
        bindings[field('start_0')] = 'start_0';
        bindings[field('start_1')] = 'start_1';
        bindings[field('end_0')] = 'end_0';
        bindings[field('end_1')] = 'end_1';
        bindings[field('DELETE')] = 'del';

        return bindings;

    };

    SpanView.prototype.field_selector = function(field_name) {
        return '#id_' + this.el.id + '-' + field_name;
    };

    var get_date = function(date) {
        return moment(date).format('YYYY-MM-DD');
    };

    var get_time = function(date) {
        return moment(date).format('HH:mm:ss');
    };


    // TODO: move to model
    var span_to_timeline_attrs = function(span) {
        return {
            start: date_from_split_values(span.attributes.start_0, span.attributes.start_1),
            end: date_from_split_values(span.attributes.end_0, span.attributes.end_1),
            content: span.attributes.slug,
            className: span.attributes.del ? 'st-delete' : '',
            editable: span.attributes.del ? false : true
        };
    };

    var timeline_attrs_to_span = function(attrs) {
        return {
            start_0: get_date(attrs.start),
            start_1: get_time(attrs.start),
            end_0: get_date(attrs.end),
            end_1: get_time(attrs.end)
        };
    };

    var TimelineView = TimeCop.TimelineView = Backbone.View.extend({});

    TimelineView.TIMELINE_OPTIONS = {
        axisOnTop: true,
        editable: true,
        minHeight: 200,
        showButtonNew: false,
        showNavigation: true
    };

    TimelineView.prototype.initialize = function(options) {
        this.timeline_options = _.extend({}, TimelineView.TIMELINE_OPTIONS, options.timeline_options);
        this.timeline = new links.Timeline(this.$el[0]);

        this.listenTo(this.collection, 'change', this.handle_model_change);
        links.events.addListener(this.timeline, 'change', this.handle_timeline_change.bind(this));
        links.events.addListener(this.timeline, 'delete', this.handle_timeline_delete.bind(this));
    };

    TimelineView.prototype.render = function() {
        var data = this.collection.map(span_to_timeline_attrs);
        this.timeline.draw(data, this.timeline_options);
    };

    TimelineView.prototype.listen_to_changes = function() {
        this.listenTo(this.collection, 'change', this.handle_model_change);
    };

    TimelineView.prototype.ignore_changes = function() {
        this.stopListening(this.collection);
    };

    TimelineView.prototype.handle_model_change = function(model) {
        this.timeline.changeItem(model.attributes.index, span_to_timeline_attrs(model));
    };

    TimelineView.prototype.handle_timeline_change = function() {
        var index = this.get_selected_index();
        if(index !== undefined) {
            // temporarily ignore model changes to avoid the cycle
            // timeline update -> model update -> timeline update
            this.ignore_changes();
            this.update_model(index, this.timeline.getItem(index));
            this.listen_to_changes();
        }

    };

    TimelineView.prototype.handle_timeline_delete = function() {
        var index = this.get_selected_index();
        if(index !== undefined) {
            this.collection.at(index).set('del', true);
             // cancel because we don't actually want to remove the
             // object from the timeline -- it will be tombstoned instead.
            this.timeline.cancelDelete();
            this.timeline.setSelection([]);
        }
    };

    TimelineView.prototype.update_model = function(index, span_data, options) {
        this.collection.at(index).set(timeline_attrs_to_span(span_data), options);
    };

    TimelineView.prototype.get_selected_index = function() {
        var selection = this.timeline.getSelection();
        return selection.length ? selection[0].row : undefined;
    };

}).call(this);
