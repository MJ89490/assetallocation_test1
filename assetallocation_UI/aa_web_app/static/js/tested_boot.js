$(document).ready(function(){
  var i=1;

  $("#add_row").click(function(){
  var numTr = $("#tab_logic tbody tr").length;


  $('#tab_logic').append("</td><td><input  name='mobile"+numTr+"' type='text' placeholder='Mobile'  class='form-control input-md'></td></tr>");




});


 $("#show_data").click(function(){
    var htmlString="";
     var lag = parseInt(document.getElementById('mobile').value);
     console.log(lag);
    $("#tab_logic tbody tr").each(function(index,el){
       if(index<$("#tab_logic tbody tr").length) {
          var mobile = $("[name='mobile"+index+"']").val();
          console.log("Row "+index+" : [Mobile="+mobile+"]");
       }

    });
 });
});