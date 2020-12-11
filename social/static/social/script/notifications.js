$(document).ready(function(){


    $("#clear_btn").click(function(){

        $.ajax(
        {
            type:"GET",
            url: "/clear_notification/",
            data:{
                },
            success: function( data )
            {
                if(data.cleared=='True')
                {
                    $(".all_notification").addClass("d-none");
                }
                else
                {

                }

            }
         })
    });



});