$(document).ready(function(){

   $('#setting_btn').click(function () {
                  $(".card-columns").css("column-count", "3");
                  $("#show-note-box" ).css("height", "5%");
                  $("#note-box" ).css("height", "20%");
                  $("#grid_list_btn").show();
                  $("#setting_btn").hide();

   });
   $('#grid_list_btn').click(function () {
               $(".card-columns").css("column-count", "1");
               $("#show-note-box" ).css("height", "2%");
               $("#note-box" ).css("height", "10%");
               $("#setting_btn").show();
               $("#grid_list_btn").hide();
   });

});