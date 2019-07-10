// set the first nav item as active
// let dis = $(".list-wrap li").eq(0);

// align the wave
// align(dis);

// align the wave on click

window.onload = function () {
    let main_body = $("body");
    main_body.css('background', '#70a1ff');
    let li_wrap = $(".list-wrap li"), dis;
    // console.log(li_wrap);
    li_wrap.click(function () {
        // console.log("click");
        dis = $(this);
        align(dis);
    });

    function align(dis) {

        // add active class to the new item
        li_wrap.removeClass("active");
        dis.delay(100).queue(function () {
            dis.addClass('active').dequeue();
        });


        // ▼ this is not necessary for the navigation ▼

        // set the background color
        let color = dis.data('color');
        console.log(dis);
        main_body.css('background', color);

        // set the text
        $(".page").text(dis.attr("title"));
        $("#show_page").attr("src", dis.attr("title"));
    }
};

