/**
 * Created by echernib on 9/7/16.
 */

$(document).ready(function () {
    $(".clickable-div").click(function(e) {
        if (e.ctrlKey) {
            window.open($(this).find("a:last").attr("href"), "_blank");
        } else {
            window.location.href = $(this).find("a:last").attr("href");
            return false;
        }
    });

    $(".clickable-div").hover(function () {
        $(this).attr("title", $(this).find("a:last").attr("href"));
        window.status = $(this).find("a:last").attr("href");
    });

    $(".clickable-div").css("cursor", "pointer");

    $(".inside-link").click(function(event){
        event.stopImmediatePropagation();
    });
});
