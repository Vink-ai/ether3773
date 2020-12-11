$(document).ready(function(){

    $('#msg_body').scrollTop($('#msg_body')[0].scrollHeight);

    setTimeout(message,500);

    var input_message = document.getElementById("msg_input");
    input_message.addEventListener("keyup", function(event) {
      if (event.keyCode === 13) {
       event.preventDefault();
       document.getElementById("send_btn").click();
      }
    });

    $("#send_btn").click(function(){
        var msg,rid;
        rid = $(this).attr("data-rid");
        msg = $("#msg_input").val();
        $.ajax(
        {
            type:"GET",
            url: "/sendMessage/",
            data:{
                     rec_id: rid,
                     message: msg
                },
            success: function(data)
            {
                if (data.sent == "True")
                {
                    $("#msg_input").val("")
                }
            }
         })
     });

});

function message(){
    var rid ,ppid;
    ppid = $("#pvr").attr("data-ppid");
    rid =  $("#pvr").val();

     $.ajax({
      type: 'get',
      url: '/messageFetch/',
      data:{
           rec_id: rid,
      },
      success: function(output){
        for(var i=0;i<output.length;i++)
        {
            if(output[i].rec == "True")
            {
                $( ".message-body" ).append( '<div class="receiver-block" style="width:70%;float: left;margin: .5rem .1rem;"><span style="float: left;" ><a href="/profile/'+rid+'"><img class="rec-icon" src="/media/'+ppid+'"></a></span><h5 class="receiver-msg" >'+output[i].msg+'</h5></div>' );
                $('#msg_body').scrollTop($('#msg_body')[0].scrollHeight);
            }
            else
            {
                $( ".message-body" ).append( '<div class="sender-block" style="width:70%;float: right;margin: .5rem .1rem;"><h5 class="sender-msg" >'+output[i].msg+'</h5></div>' );
                $('#msg_body').scrollTop($('#msg_body')[0].scrollHeight);
            }
        }

      },
      complete:function(data){
        setTimeout(message,500);
      }
     });
}