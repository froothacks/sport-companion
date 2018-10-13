$(document).ready(function() {
    console.log("Hello");
    $("#submit").click(login.authenticate)
});

login = {
    authenticate: function (params) {
        var email = ("#inputEmail").val
        var password = ("#inputPassword").val
        alert(email, password);
        var saveData = $.ajax
        ({
            type: 'POST',
            url: "",
            data: {
                "email": email,
                "password": password
            },
            dataType: "json",
            success: function (resultData) {
                alert("Save Complete")
            }
        });
        
    }
}