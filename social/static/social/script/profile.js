$(document).ready(function(){

              for(var i=1 ;i<6 ;i++){
                    $('#heading'+i.toString()).hide();
               }
              $('#heading'+'1').show();

              $('#new_img').hide();
              $('#default_foot2').hide();
              $("#input_txt").hide();


              $('#update_prof_btn').hide();
              $('#preview_profile').hide();


              $(".nav-link").click(function(){
                $("#navbarTogglerDemo02").hide();
              });

              $(".navbar-toggler").click(function(){
                $("#navbarTogglerDemo02").toggle();
              });


               $("#profile_pic").click(function(){
                    $('#preview_profile').hide();
                    $('#original_profile').show();
                    $('#change_prof_btn').show();
                    $('#update_prof_btn').hide();
                });


               function readURL(input,path) {
                    if (input.files && input.files[0]) {
                        var reader = new FileReader();

                        reader.onload = function (e)
                        {
                            if(path == "post_img")
                            {
                                $('#new_img').attr('src', e.target.result);
                                $('#new_img').show();
                                $('#post_default').hide();
                                $('#default_foot').hide();
                                $('#post_text').hide();
                                $('#default_foot2').show();
                                $('#img_sub').show();
                                $('.sub_hr').show();
                                $('#img_sub').focus();
                            }
                            if(path == "preview_profile")
                            {
                                $('#preview_profile').attr('src', e.target.result);
                                $('#preview_profile').show();
                                $('#original_profile').hide();
                                $('#change_prof_btn').hide();
                                $('#update_prof_btn').show();
                            }
                        }
                        reader.readAsDataURL(input.files[0]);
                    }
                }


              $("#post_img").click(function(){
                $("#input_img").click();
              });

               $("#input_img").change(function(){
                    readURL(this,"post_img");
                });

                $("#post_cancel").click(function(){
                    $("#default_foot2").hide();
                    $("#default_foot").show();
                    $('#new_img').attr('src', '');
                    $('#input_img').val('')
                    $('#new_img').hide();
                    $('#post_default').show();
                    $("#input_txt").hide();
                    $('html, body').animate({
                        scrollTop: $("#default_foot").position().top
                    });
                });

                $("#post_txt").click(function(){
                    $("#input_txt").show();
                    $("#input_txt").focus();
                    $('#post_default').hide();
                    $('#default_foot').hide();
                    $('#default_foot2').show();
                    $('#img_sub').hide();
                    $('.sub_hr').hide();
                });

                $("#change_prof_btn").click(function(){
                    $("#update_prof_input").click();
                });

               $("#update_prof_input").change(function(){
                    readURL(this,"preview_profile");
               });


               $('.follow_btn').click(function(){
                    var pid;
                    pid = $(this).attr("data-pid");
                    $.ajax(
                    {
                        type:"GET",
                        url: "/profile/follow_operation/",
                        data:{
                                 prof_id: pid,
                                 operation:'follow'
                            },
                        success: function( data )
                        {
                            if(data.requested=='True')
                            {
                                $(".requested").removeClass("d-none");
                                $(".follow").addClass("d-none");
                            }
                        }
                     })
                });

                $(".accept_req_btn").click(function(){
                    var pid;
                    pid = $(this).attr("data-pid");
                    $.ajax(
                    {
                        type:"GET",
                        url: "/profile/follow_operation/",
                        data:{
                                 prof_id: pid,
                                 operation:'accept_req'
                            },
                        success: function( data )
                        {
                            if(data.accepted=='True')
                            {
                                $(".accept_req").addClass("d-none");
                                $(".accept_req2").removeClass("d-none");
                            }
                        }
                     })
                });

                $(".f-option").click(function(){
                    var pid,opt;
                    pid = $(this).attr("data-pid");
                    opt = $(this).attr("data-opt");
                    $.ajax(
                    {
                        type:"GET",
                        url: "/profile/follow_operation/",
                        data:{
                                 prof_id: pid,
                                 operation:opt
                            },
                        success: function( data )
                        {
                            if(data.unfollowed=='True')
                            {
                                window.location.reload();
                            }
                            else if(data.rejected=='True')
                            {
                                window.location.reload();
                            }
                            else if(data.cancel_req=='True')
                            {
                                window.location.reload();
                            }
                            else if(data.rejected=='True')
                            {
                                window.location.reload();
                            }
                        }

                     })
                });


                $(".like").click(function(){
                    var pid,prid,nm,myp,mypp;
                    nm = $(this).attr("data-mynm").toString();
                    myp = $(this).attr("data-myp").toString();
                    mypp = $(this).attr("data-mypp").toString();
                    pid = $(this).attr("data-id");
                    prid = $(this).attr("data-pid");
                    $.ajax(
                    {
                        type:"GET",
                        url: "/like_post/",
                        data:{
                                 post_id: pid,
                                 prof_id: prid
                            },
                        success: function( data )
                        {
                            if(data.liked=='True')
                            {
                                $(".like"+pid.toString()).addClass("ticked");
                                document.getElementById("l"+pid.toString()).innerHTML = data.l_count;
                                $( ".pt"+pid.toString() ).append('<div class="t'+myp+'p'+pid.toString()+'" style="padding:.5rem; border-bottom: .5px solid #cecece;"><a class="tc fs a-link" href="/profile/'+myp+'" ><span style="align-self: center;" ><img class="profile-icon" src="'+mypp+'"> </span>'+nm+'</a></div>')
                            }
                            else if(data.liked=='False')
                            {
                                $(".like"+pid.toString()).removeClass("ticked");
                                document.getElementById("l"+pid.toString()).innerHTML = data.l_count;
                                $(".t"+myp+"p"+pid.toString()).addClass("d-none");
                            }

                        }
                     })
                });

                 $(".comment-noty").click(function(){
                    var cid;
                    cid = $(this).attr("data-cn");
                    $(".comment-block"+cid.toString()).toggleClass("d-none");
                    window.scrollBy(0, 100);
                 });

                 $(".comment-btn").click(function(){
                    var cid;
                    cid = $(this).attr("data-cid");
                    $( ".comment-block"+cid.toString() ).removeClass("d-none");
                    $( "#comment-input"+cid.toString() ).focus();
                 });


                 $(".comment-send").click(function(){
                    var pid,prid,cmt,nm,myp,mypp;
                    nm = $(this).attr("data-mynm").toString();
                    myp = $(this).attr("data-myp").toString();
                    mypp = $(this).attr("data-mypp").toString();
                    pid = $(this).attr("data-id");
                    prid = $(this).attr("data-pid");
                    cmt = $("#comment-input"+pid.toString()).val();
                    $.ajax(
                    {
                        type:"GET",
                        url: "/comment_post/",
                        data:{
                        
                                 post_id: pid,
                                 prof_id: prid,
                                 cmt: cmt
                            },
                        success: function( data )
                        {
                            if(data.commented=='True')
                            {
                                $( ".comment-box" ).append( '<div class="comments" ><span><a href="'+myp+'"> <img style="width:1.5rem;height:1.5rem;border-radius:3rem;" src="'+mypp+'"> </a></span><a class="tc cp fs a-link" href="'+myp+'" > '+nm+'&nbsp:&nbsp</a><p class="m-0" style=" text-align: initial; padding: 0 .5rem;">'+cmt+'</p></div>' );
                                $("#comment-input"+pid.toString()).val("")
                                document.getElementById("c"+pid.toString()).innerHTML = data.c_count;
                                $('#cmt_body'+pid.toString()).scrollTop($('#cmt_body'+pid.toString())[0].scrollHeight);
                            }

                        }
                     })
                 });





        });

        function heading(index){
            for(var i=1 ;i<6 ;i++){
                $('#heading'+i.toString()).hide();
            }
            $('#heading'+index).show();
        }
