$.fn.dashboard = function (element, initial_settings, save_url) {

    $.fn.dashboard.widgets_init = {};
    $.fn.dashboard.save_url = save_url;
    $.fn.dashboard.load_state(initial_settings);
};
$.fn.dashboard.setup_widgets_modal = function () {
    /*
     Sets up Widgets Modal listing all available widgets
     */
    var available_widgets = $.fn.dashboard.get_available_widgets();
    var installed_widgets = $.fn.dashboard.get_installed_widgets();
    var widget_install_button = '';
    var list_item = '';
    var install_widgets_list = $("#install_widgets_list");
    install_widgets_list.empty();
    $.each(available_widgets, function (index, widget) {
        if ($.inArray(widget.id, installed_widgets) > -1)
            widget_install_button = '<a href="#" class="btn btn-success pull-right widget-install-btn disabled" data-id=' + widget.id + '><i class="glyphicon glyphicon-plus"></i> Added</a>';
        else
            widget_install_button = '<a href="#" class="btn btn-success pull-right widget-install-btn" data-id=' + widget.id + '><i class="glyphicon glyphicon-plus"></i> Add Widget</a>';
        var circle = "";
        if (widget.newWidget) {
            circle = '<span class="pull-right new_marker">New</span>';
        }
        list_item = '<li class="list-group-item">' + widget_install_button + circle + '<h5>' + widget.name + '</h5><span class="description">' + widget.description + '</span></li>';
        install_widgets_list.append(list_item);
    });

    install_widgets_list.find('.widget-install-btn').each(function () {
        $(this).on('click', function () {
            $.fn.dashboard.add_widget($(this).data('id'), 'column-2', $(this).data('options'));
            $(this).addClass('disabled').html('<i class="glyphicon glyphicon-plus"></i> Added</a>');
            $.fn.dashboard.save_state();
        });

    });
    $.fn.dashboard.setup_global_widget_options();
    $("#load_modal").modal();
};

$.fn.dashboard.get_widget_settings = function () {
    /*
     Returns the current configuration of all the widgets attached to the dashboard

     example:
     {
     'column-1': {
     {
     'id': 1,
     'collapsed': true,
     },
     {
     'id': 2,
     'collapsed': true,
     },

     },
     'column-2': {},
     }
     */
    var widget_settings = {
        'column-1': {},
        'column-2': {}
    };
    var column_counter = 0;
    $("#column-1").find(".panel").each(function () {
        widget_settings['column-1'][column_counter] = {
            'id': $(this).data('id'),
            'collapsed': $(this).data('collapsed'),
            'options': $(this).data('options')
        };
        column_counter += 1;
    });
    column_counter = 0;
    $("#column-2").find(".panel").each(function () {
        widget_settings['column-2'][column_counter] = {
            'id': $(this).data('id'),
            'collapsed': $(this).data('collapsed'),
            'options': $(this).data('options')
        };
        column_counter += 1;
    });
    return widget_settings
};

$.fn.dashboard.add_widget = function (widget_id, column_id, collapsed, saved_options) {
    /*
     Clones a copy of one the preloaded hidden widgets, appends it the dashboard and toggles it.
     */
    var widget = $("#" + widget_id).clone(false).removeAttr('id').data('id', widget_id).removeClass('hide');
    if (collapsed == false) {
        widget.data('collapsed', collapsed);
    }
    if (collapsed != undefined) { // if undefined we're adding widgets from modal else its the initial state loading
        $('#' + column_id).append(widget);
    } else {
        $('#' + column_id).prepend(widget);

    }
    $.fn.dashboard.setup_global_widget_options();
    if (saved_options == undefined) {
        saved_options = {};
    }
    var options = {};
    widget.save = $.fn.dashboard.save_state;
    widget.defaults = window[widget_id + '_defaults'];
    $.each(widget.defaults, function (option, value) {
        if (option in saved_options) {
            options[option] = saved_options[option]
        } else {
            options[option] = value

        }

    });
    widget.data('options', options);
    window[widget_id + '_init'](widget, options);
};

$.fn.dashboard.get_available_widgets = function () {
    var available_widgets = [];
    $("#available-widgets").find(".panel").each(function () {
        var newWidget = false;
        if ($(this).hasClass("new-widget")) {
            newWidget = true;
        }
        available_widgets.push({
            'id': $(this).attr('id'),
            'name': $(this).data('name'),
            'description': $(this).data('description'),
            'newWidget': newWidget
        });
    });
    return available_widgets
};

$.fn.dashboard.get_installed_widgets = function () {
    var installed_widgets = [];
    $("#installed-widgets").find(".panel").each(function () {
        installed_widgets.push($(this).data('id'));
    });
    return installed_widgets
};

$.fn.dashboard.load_extra_plugins = function () {
    /*
     We can add any additional plugins that we need to load here
     */
};

$.fn.dashboard.setup_global_widget_options = function () {
    /*
     Loads widget options common between all widgets

     Makes the widget portable
     flags its listing in the modal as installed
     loads additional plugins
     */
    var panelList = $('#column-1, #column-2');
    panelList.sortable({

        connectWith: ".draggablePanelList",
        placeholder: "ui-state-highlight",
        handle: '.panel-heading',
        update: function () {
            $('.panel').each(function (index, elem) {
                var $listItem = $(elem),
                    newIndex = $listItem.index();
            });
            $.fn.dashboard.save_state();
        }
    });
    var installed_widgets = $('#installed-widgets');
    installed_widgets.find('.minimize-widget-toggle').each(function () {
        var widget = $(this).parents('.panel');
        var widget_body = widget.children('.panel-body');
        if (widget.data('collapsed') == true) {
            widget_body.show();
            $(this).find('.fa').addClass('fa-chevron-down');
            $(this).find('.sr-only').text('Minimize');
        } else {
            widget_body.hide();
            $(this).find('.fa').addClass('fa-chevron-right');
            $(this).find('.sr-only').text('Collapse');

        }
        $(this).unbind('click').on('click', function () {

            if (widget.data('collapsed') == true) {
                widget_body.hide();
                $(this).find('.fa-chevron-down').removeClass('fa-chevron-down').addClass('fa-chevron-right');
                widget.data('collapsed', false);
                $(this).find('.sr-only').text('Collapse');
            } else {
                widget_body.show();
                $(this).find('.fa-chevron-right').removeClass('fa-chevron-right').addClass('fa-chevron-down');
                widget.data('collapsed', true);
                $(this).find('.sr-only').text('Minimize');

            }
            $.fn.dashboard.save_state();
        });
    });

    installed_widgets.find('.close-widget-toggle').each(function () {
        $(this).unbind('click').on('click', function () {
            $(this).parents('.panel').remove();
            $.fn.dashboard.save_state();
        });
    });

    jQuery("abbr.timeago").timeago();
    $.fn.dashboard.load_extra_plugins();
};


$.fn.dashboard.save_state = function () {
    var widget_settings = $.fn.dashboard.get_widget_settings();
    $.ajax({
        url: $.fn.dashboard.save_url,
        data: {'widget_settings': JSON.stringify(widget_settings)},
        type: "POST"
    })
};
$.fn.dashboard.load_state = function (initial_settings) {
    /*
     loads the widgets saved in the user profile (usermeta.widget_settings)
     */
    var widget_settings = JSON.parse(initial_settings);
    $.each(widget_settings, function (column_index, column) {
        $.each(column, function (index, widget) {
            $.fn.dashboard.add_widget(widget.id, column_index, widget.collapsed, widget.options);
        })
    })
};