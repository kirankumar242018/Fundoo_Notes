$(document).ready(function(){

     $("#add-collaborator").click(function (e){
        $("#note-box").hide();
        $("#collaborator").show();
     });


      $("#save-btn").click(function (e){
        $("#collaborator").hide();
        $("#note-box").show();
     });

      $("#cancel-btn").click(function (){
        $("#collaborator").hide();
        $("#note-box").show();
     });
});