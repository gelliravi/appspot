function show_example(gid) {
    $('#gid').val(gid);
    submit();
};

function reset() {
    window.location = "/athaliana";
};

function submit() {
    var url = '/athaliana/query'
    var params = $('form').serialize();
    $('#response').html();

    window.location = url + "?" + params;
};

function page(p, query_str) {
    var url = '/athaliana/query'
    var params = query_str + '&page=' + p; 
    $('#response').html();
    
    window.location = url + "?" + params;
}

$(function() {
    $("button, input[type=submit], input[type=reset]").button();
    $(".radio").buttonset();

    $("input#gid").autocomplete({
        source: "/athaliana/autocomplete"
    });
});
