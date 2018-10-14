$(document).ready(function () {
    $("#create_event").click(function () {
        modal.inflate();
    });
    $("#success-btn").click(function () {
        sports.create_event();
    });
    // $('#datetimepicker1').click(function() {$('#datetimepicker1').datetimepicker({uiLibrary: 'bootstrap4'});})
    // // $("#date_entry").datepicker({
    // //     beforeShow: function() {
    // //     setTimeout(function(){
    // //         $('.ui-datepicker').css('z-index', 99999999999999);
    // //     }, 0);}});
    var selectValues = ["archery", "badminton", "baseball and softball", "basketball", "beach volleyball", "boxing", "canoe / kayak", "climbing", "cycling", "diving", "golf", "gymnastics", "handball", "judo", "karate", "roller sport", "rowing", "sailing", "shooting", "soccer / football", "swimming", "surfing", "synchronized swimming", "table tennis", "taekwondo", "tennis", "track and field", "triathlon", "water polo", "weightlifting", "wrestling"]
    $.each(selectValues, function (key, value) {
        $('#event_type')
            .append($("<option></option>")
                .attr("value", value)
                .text(value));
    });
});


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
        var saveData = $.ajax({
            type: 'POST',
            url: "/create_event",
            data: {
                'type': $("#event_type").val(),
                'date': $("#entry").val(),
                'location': $("#loc").val(),
                'duration': $("#dur").val()
            },
        });
    }
};

modal = {

    inflate: function () {
        $("#myModal").modal();
    }
};