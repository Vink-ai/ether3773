$(document).ready(function(){

    function readURL(input,path) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();

            reader.onload = function (e)
            {
                if(path == "profile_img")
                {
                     $('#profile_img').attr('src', e.target.result);
                }
                if(path == "cover_img")
                {
                    $('#cover_img').attr('src', e.target.result);
                }
            }
            reader.readAsDataURL(input.files[0]);
        }
    }

    $("#cover_change").click(function(){
        $("#cover_input").click();
    });

    $("#cover_input").change(function(){
        readURL(this,"cover_img");
    });

    $("#profile_change").click(function(){
        $("#profile_input").click();
    });

    $("#profile_input").change(function(){
        readURL(this,"profile_img");
    });

    $("#pas_change").click(function(){
        var opas,npas;
        opas = $("#opassword").val();
        npas = $("#npassword").val();
        $.ajax(
        {
            type:"GET",
            url: "/changePassword/",
            data:{
                     opassword: opas,
                     npassword: npas,
                },
            success: function( data )
            {
                if(data.password_error != '')
                {
                    document.getElementById("pass_error").innerHTML = data.password_error;
                }
                else
                {
                    document.getElementById("pass_error").innerHTML = "";
                }
                if(data.password_error2 != '')
                {
                    document.getElementById("pass_error2").innerHTML = data.password_error2;
                }
                else
                {
                    document.getElementById("pass_error2").innerHTML = "";
                }
                if(data.password_error == '' && data.password_error2 == '')
                {
                    window.location.href = document.getElementById('logout').href;
                }

            }
         })
     });



});