$(document).ready(function () {
    $("#create_event").click(function () {
        modal.inflate();
    });
    $("#success-btn").click(function () {
        sports.create_event();
    });
    sports.render_activities($("#grid"));
    var selectValues = ["football", "badminton", "basketball", "bicycle", "bowling", "soccer", "weight-training", "running", "swimming"]
    $.each(selectValues, function (key, value) {
        $('#event_type')
            .append($("<option></option>")
                .attr("value", value)
                .text(value));
    });
});


sports = {
    render_item: function ($elm, title, time, location, id, joined) {
        var cssc = ""
        for (let i = 0; i < joined.length; i++) {
            console.log("LL", id, joined[i])
            if (id === joined[i]) {
                cssc = " disabled"
            }
        }
        console.log(title);
        console.log($elm);
        $($elm).append(//`<div> test </div>`);
            `<div class="col-lg-3 col-md-6 mb-4">
    <div class="card"><a href="#"><img class="card-img-top" src="/static/images/`+title+`.png" alt=""></a>
        <div class="sport-name">` + title + `</div>
        <div>Time:` + time + `</div>
        <div>Location:` + location + `</div>
<button data-id=` + id + ` class="join btn btn-success `+cssc+"\""+`>Join Event</button>
</div>`);

    },
    render_activities: function ($elm) {
        $.get("/events", function (data) {
            console.log(data);
            data = JSON.parse(data);
            let joined = data.joined;
            data = data.result;
            console.log("Hj", joined);
            for (let index = 0; index < data.length; index++) {
                sports.render_item($elm, data[index].name, data[index].time, data[index].location, data[index].id, joined)
            }
            $(".join").click(function () {
                $(this).addClass("disabled");
                var saveData = $.ajax({
                    type: 'POST',
                    url: "/join",
                    data: {
                        'event-id': ($(this).attr("data-id"))
                    },
                });

            })
        });
    },
    create_event: function () {
        var saveData = $.ajax({
            type: 'POST',
            url: "/create_event",
            data: {
                'type': $("#event_type").val(),
                'date': $("#entry").val(),
                'location': $("#loc").val(),
                'duration': $("#dur").val()
            },
            success: function () {
                location.reload();
            }
        });

    }
};

modal = {

    inflate: function () {
        $("#myModal").modal();
    }
};