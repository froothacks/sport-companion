// $(document).ready(function() {
//     console.log("Hello");
//     $("#submit").click(login.authenticate)
// });
//
// login = {
//     authenticate: function (params) {
//         var email = $("#inputEmail").val();
//         var password = $("#inputPassword").val();
//         if (email === "" || password === ""){return;}
//         console.log(email, password);
//         var saveData = $.ajax
//         ({
//             type: 'POST',
//             url: "http://127.0.0.1:5000/auth",
//             data: {
//                 "email": email,
//                 "password": password
//             },
//             dataType: "json",
//             success: function (resultData) {
//                 alert("Save Complete")
//             },
//             error: function(resultData){
//                 console.log(resultData)
//             }
//         });
//
//     }
// }