$(document).ready(function () {
    try {
        $('#id_supervisor').select2('destroy');
    } catch (e) {
        //Ignore otherwise
    }

    $('a#offline_approve').click(function () {
        $("#load_offline_modal").modal();
    });

    $('a#return').click(function () {
        $("#load_return_modal").modal();
    });

    $('a#reject').click(function () {
        $("#load_reject_modal").modal();
    });

    $('form#management').submit(function () {
        $('.management-buttons').children().hide();
        $('#modify').hide();
        $('#waiting').show();
    });

    $('.modal input[name$="details"]').keypress(function (e) {
        if (e.which == 13) {
            e.preventDefault();
            $(e.target).parents('.modal').find('button[type="submit"]').click();
        }
    });
});

