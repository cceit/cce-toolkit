function initialize_plugins(advanced_search_form_bound) {
    $('.datefield').each(function (index, value) {
        $(this).datepicker({
            format: "mm/dd/yyyy",
            todayBtn: "linked",
            autoclose: true,
            todayHighlight: true
        });
        $(this).data('has_datepicker', true)
    });
    $('.tinymce').each(function (index, value) {
        initTinyMCE($(this));
    });
    $("select").select2();

    // fix for report selector. We disable select2
    $(".report_selector select").select2("destroy");

    $('.timefield').datetimepicker({
        format: 'LT'
    });

    $('.datetimefield').datetimepicker({
        format: 'MM/DD/YYYY hh:mm A'
    });

    var $advance_search_toggle = $('#advance_search_toggle');
    var $advanced_search_form = $('#advanced_search_form');

    $advance_search_toggle.on('click', function () {
        if ($advance_search_toggle.attr('aria-pressed') == 'false') {
            $advance_search_toggle.attr('aria-pressed', 'true');
            $advance_search_toggle.children('span').removeClass('glyphicon-plus');
            $advance_search_toggle.children('span').addClass('glyphicon-minus');
        } else {
            $advance_search_toggle.attr('aria-pressed', 'false');
            $advance_search_toggle.children('span').removeClass('glyphicon-minus');
            $advance_search_toggle.children('span').addClass('glyphicon-plus');
        }

        $('#advanced_search_form').toggle()
    });

    if (advanced_search_form_bound) {

        $advance_search_toggle.attr('aria-pressed', 'true');
        $advance_search_toggle.children('span').removeClass('glyphicon-plus');
        $advance_search_toggle.children('span').addClass('glyphicon-minus');
    }
    else {
        $advanced_search_form.toggle();
    }

    $(document).on("click", ".popover .close" , function(){
        $(this).parents(".popover").popover('hide');
    });

    //Help Text Popovers
    $('a[id$="_popover"] i').on("click", function(){
        $(this).parents("a").popover('toggle');
    });

    //This is needed for accessibility on the modals
    $('.modal').on('shown.bs.modal', function () {
        $('.modal .close').focus()
    });

    //Formset Remove Button
    $('.remove-btn').on('click', function (e) {
        var $parent_div = $(this).closest("div[id$='-row']");
        var $delete_input = $parent_div.find("input[id$='-DELETE']");
        $delete_input.attr('checked', 'checked');
        $parent_div.hide()
    });

    //Initialize popovers
    $(function () {
      $('[data-toggle="popover"]').popover('show')
    });

}

// function enables tinymce with settings loaded from widget, taken from django-tinymce
function initTinyMCE($e) {
    if ($e.parents('.empty-form').length == 0) {  // Don't do empty inlines
      var mce_conf = $.parseJSON($e.attr('data-mce-conf'));
      var id = $e.attr('id');
      if ('elements' in mce_conf && mce_conf['mode'] == 'exact') {
        mce_conf['elements'] = id;
      }
      if ($e.attr('data-mce-gz-conf')) {
        tinyMCE_GZ.init($.parseJSON($e.attr('data-mce-gz-conf')));
      }
      if (!tinyMCE.editors[id]) {
        tinyMCE.init(mce_conf);
      }
    }
}

function disable_plugins(){
    // disable tinymce
    $('.tinymce').each(function (index, value) {
        tinyMCE.EditorManager.execCommand('mceRemoveEditor',true, $(this).attr('id'));
    });
    // disable select2
    $("select").select2('destroy');
}

function addForm(btn, prefix) {
    // disable js plugin that are not compatible with .clone
    disable_plugins();

    // Get the div surrounding the formset
    var forms_container = $('#' + prefix);
    // Get the hidden input saying how many forms there are
    var total_forms = $('#id_' + prefix + '-TOTAL_FORMS');
    // Clone the first form to make a new form
    var newElement = forms_container.children('.dynamic-form:first').clone(false);

    // Configure the attributes of the new form as appropriate
    var total = total_forms.val();
    // The id of the form
    newElement.attr('id', newElement.attr('id').replace('-0-', '-' + total + '-'));
    // The attributes of each form element (":input" is a jQuery selector)
    newElement.find(':input').each(function () {
        var attr = $(this).attr('name');

        // For some browsers, `attr` is undefined; for others,
        // `attr` is false.  Check for both.
        if (typeof attr !== typeof undefined && attr !== false) {
            var name = $(this).attr('name').replace('-0-', '-' + total + '-');
            var id = 'id_' + name;
            $(this).attr({'name': name, 'id': id}).val('').removeAttr('checked');
        }
    });

    newElement.find(':checkbox').each(function () {
        $(this).removeAttr('value');
    });
    // The "for" attribute on each label, since ids changed
    newElement.find('label').each(function () {
        var newFor = $(this).attr('for').replace('-0-', '-' + total + '-');
        $(this).attr('for', newFor);
        // Remove datepicker... from the label? This line might not be doing anything.
        $(this).datepicker("remove");
    });

    // Update the number of forms there are
    total++;
    total_forms.val(total);
    // Put the new form on the page
    forms_container.children('.dynamic-form:last').after(newElement);

    // re-enable plugins
    initialize_plugins(false);
    return newElement;
}

function addFormV2(btn, prefix) {
    // disable js plugin that are not compatible with .clone
    disable_plugins();

    // Get the div surrounding the formset
    var forms_container = $('#' + prefix);
    // Get the hidden input saying how many forms there are
    var total_forms = $('#id_' + prefix + '-TOTAL_FORMS');
    // Clone the form seed to make a new form
    var newElement = forms_container.find("div[id$='-seed']").clone(false);
    // Configure the attributes of the new form as appropriate
    var total = total_forms.val();
    // Format the id of the form
    newElement.attr('id', newElement.attr('id').replace('-0-', '-' + total + '-'));
    newElement.attr('id', newElement.attr('id').replace('seed', 'row'));
    // The attributes of each form element (":input" is a jQuery selector)
    newElement.find(':input').each(function () {
        var attr = $(this).attr('name');

        // For some browsers, `attr` is undefined; for others,
        // `attr` is false.  Check for both.
        if (typeof attr !== typeof undefined && attr !== false) {
            var name = $(this).attr('name').replace('-0-', '-' + total + '-');
            var id = 'id_' + name;
            $(this).attr({'name': name, 'id': id}).val('').removeAttr('checked');
        }
    });

    newElement.find(':checkbox').each(function () {
        $(this).removeAttr('value');
    });
    // The "for" attribute on each label, since ids changed
    newElement.find('label').each(function () {
        var newFor = $(this).attr('for').replace('-0-', '-' + total + '-');
        $(this).attr('for', newFor);
        // Remove datepicker... from the label? This line might not be doing anything.
        $(this).datepicker("remove");
    });

    // Update the number of forms there are
    total++;
    total_forms.val(total);
    // Put the new form on the page
    forms_container.children('.dynamic-form:last').after(newElement);
    newElement.show();

    // re-enable plugins
    initialize_plugins(false);
    return newElement;
}

function deleteForm(btn, prefix) {
    $(btn).parents('.dynamic-form').remove();
    var forms = $('.dynamic-form');
    $('#id_' + prefix + '-TOTAL_FORMS').val(forms.length);
    for (var i = 0, formCount = forms.length; i < formCount; i++) {
        $(forms.get(i)).children().not(':last').children().each(function () {
            updateElementIndex(this, prefix, i);
        });
    }
    return false;
}

$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie != '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) == (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }

        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
            // Only send the token to relative URLs i.e. locally.
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    }
});

function quickLook(element, xOffset, yOffset) {
    $(document).ready(function () {
        var isMobile = window.matchMedia("only screen and (max-width: 760px)");
        if (!isMobile.matches) {

            $(element)
                .hover(
                    function (e) {
                        var popover_id = $(this).data('popover');
                        var pos = $(this).position();
                        $("#" + popover_id)
                            .css("top", (pos.top + yOffset) + "px")
                            .css("left", (pos.left + xOffset) + "px")
                            .show();
                    },
                    function () {
                        var popover_id = $(this).data('popover');
                        $("#" + popover_id).hide();
                    }
                )
                .mousemove(function (e) {
                    var popover_id = $(this).data('popover');
                    var pos = $(this).position();
                    $("#" + popover_id)
                        .css("top", (pos.top + yOffset) + "px")
                        .css("left", (pos.left + xOffset) + "px")
                });
        }
    });
}

$(document).ready(function () {

    /*Scroll to the top*/
    $().UItoTop({easingType: 'easeOutQuart'});

    $('div.static-alert button.close').remove();

});