sports = {
        render_item = function ($elm, title) {
            $elm.append(
                    ```<div class="col-lg-4 col-md-6 mb-4"> <
                    div class = "card" >
                    <
                    a href = "#" > < img class = "card-img-top"
                    src = "http://placehold.it/200x100"
                    alt = "" > < /a> <
                    div class = "sport-name" >```+title+```< /div>
                    <
                    /div> <
                    /div>```);
                $elm.last().click()
                
                },
                render_activities = function ($elm) {
                    $.get("url", function (data) {
                        for (let index = 0; index < data.length; index++) {
                            sports.render_item($elm, data[index])

                            
                        }
                    });
                },
                create_event: function(){
                    
                }
        }