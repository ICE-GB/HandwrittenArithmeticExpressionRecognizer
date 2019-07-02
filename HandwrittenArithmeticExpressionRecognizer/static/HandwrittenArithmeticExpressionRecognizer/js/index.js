window.onload = function () {
    $("#upload").click(function () {
        $("#show_page").attr("src", "/upload");
    });
    $("#hand_write").click(function () {
        $("#show_page").attr("src", "/hand_write");
    });
};
