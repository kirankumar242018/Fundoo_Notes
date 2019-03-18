$(document).ready(function(){

$('#create-label').click(function () {
                  <!--$(".card-columns").css("column-count", "3");-->
                  <!--$("#show-note-box" ).css("height", "5%");-->
                  $("#create-label" ).css("border-bottom", "1px solid rgb(116, 119, 121)");
                  $("#create-label" ).css("border-radius", "1%");
                  $("#edit-label" ).css("border-bottom", "1px solid transparent");
                  $("#checkmark-btn").show();
                  $("#cancel-btn").show();
                  $("#add-btn").hide();
});

$('#cancel-btn').click(function () {
                  <!--$(".card-columns").css("column-count", "3");-->
                  <!--$("#show-note-box" ).css("height", "5%");-->
                  <!--$("#note-box" ).css("height", "12%");-->

                  $("#create-label" ).css("border-bottom", "1px solid transparent");
                  $("#checkmark-btn").hide();
                  $("#cancel-btn").hide();
                  $("#add-btn").show();
});

$('#edit-label').click(function () {
                  <!--$(".card-columns").css("column-count", "3");-->
                  <!--$("#show-note-box" ).css("height", "5%");-->
                  <!--$("#note-box" ).css("height", "12%");-->

                  $("#create-label" ).css("border-bottom", "1px solid transparent");
                  $("#edit-label" ).css("border-bottom", "1px solid rgb(116, 119, 121)");
                  $("#edit-label" ).css("border-radius", "1%");
                  $("#list-label-btn").hide();
                  $("#pencil-btn").hide();
                  $("#checkmark1-btn").show();
                  $("#delete-btn").show();
                  $("#checkmark-btn").hide();
                  $("#cancel-btn").hide();
                  $("#add-btn").show();
});

 $("#list-label-btn").mouseenter(function () {
           $("#delete-btn").show();
           $("#list-label-btn").hide();

    });

    $("#delete-btn").mouseleave(function () {
          $("#delete-btn").hide();
          $("#list-label-btn").show();

    });

    $(".modal-footer").click(function () {
         $("#create-label" ).css("border-bottom", "1px solid transparent");
         $("#edit-label" ).css("border-bottom", "1px solid transparent");
         $("#pencil-btn").show();
         $("#list-label-btn").show();
         $("#delete-btn").hide();
         $("#checkmark1-btn").hide();

    });




});