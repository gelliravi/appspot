function show_example(gid) {
    $('#gid').val(gid);
    submit();
};

function reset() {
    window.location = "/athaliana";
};

function submit() {
    var params = $('form').serialize();
    $('#response').html();

    window.location = "?" + params;
};

function page(p) {
    var params = $('form').serialize();
    params += '&page=' + p;
    $('#response').html();
    
    window.location = "?" + params;
}

$(function() {
    $("button, input[type=submit], input[type=reset]").button();
    $(".radio").buttonset();

    $("input#gid").autocomplete({
        source: "/athaliana/autocomplete"
    });
});
