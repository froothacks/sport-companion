sports = {
    render_item: function ($elm, title) {
        console.log(title);
        console.log($elm);
        $($elm).append(//`<div> test </div>`);
            `<div class="col-lg-3 col-md-6 mb-4"><div class="card"><a href="#"><img class="card-img-top" src="/static/images/basketball.png" alt=""></a><div class="sport-name">` + title + `</div></div></div>`);
        //$elm.last().click()

    },
    render_activities: function ($elm) {
        $.get("/events", function (data) {
            console.log(data);
            data = JSON.parse(data).result;
            for (let index = 0; index < data.length; index++) {
                sports.render_item($elm, data[index].name)


            }
        });
    },
    create_event: function () {

    }
};