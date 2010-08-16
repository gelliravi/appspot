function show_example(gid) {
    $('#gid').val(gid);
    submit();
};

function reset() {
    window.location = "/athaliana";
};

function submit() {
    var url = "/athaliana/query";
    var params = $('form').serialize();
    var query = url + "?" + params;
    $('#response').html();

    window.location = query;
};

$(function() {
    $("button, input[type=submit], input[type=reset]").button();
    $(".radio").buttonset();

    $("input#gid").autocomplete({
        source: "/athaliana/autocomplete"
    });
});
