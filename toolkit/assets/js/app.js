function initialize_form_plugins() {
    $('.datefield').each(function (index, value) {
        $(this).datepicker({
            format: "mm/dd/yyyy",
            todayBtn: "linked",
            autoclose: true,
            todayHighlight: true
        });
        $(this).data('has_datepicker', true)
    });
    $("select").select2();
    $('.timefield').datetimepicker({
        format: 'LT'
    });
}

function addForm(btn, prefix) {
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
        var name = $(this).attr('name').replace('-0-', '-' + total + '-');
        var id = 'id_' + name;
        $(this).attr({'name': name, 'id': id}).val('').removeAttr('checked');
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

    initialize_form_plugins();
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