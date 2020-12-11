 $(document).ready(function(){
    setTimeout(notification,1500);

});

function notification(){

 $.ajax({
  type: 'get',
  url: '/notification/fetch/',
  success: function(data){
    if(data.notification_count > 0){
        $("#notification_badge").addClass("badge2");
        document.getElementById("notification_badge").innerHTML = data.notification_count;
    }
    else{
        $("#notification_badge").removeClass("badge2");
    }
  },
  complete:function(data){
   setTimeout(notification,1500);
  }
 });

}