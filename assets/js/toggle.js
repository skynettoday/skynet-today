var displayingNews = true;
$(function() {
    var form = document.querySelector("#writingToggleForm");
    form.addEventListener("change", function(event) {
        console.log("Toggling writing display!");
        if(displayingNews){
          $('#news').fadeToggle(function() {
              $('#editorials').fadeToggle(function() {
              });
          });
        }else{
          $('#editorials').fadeToggle(function() {
              $('#news').fadeToggle(function() {
              });
          });
        }
        displayingNews = !displayingNews;
    });
    $("#editorials").fadeOut();

    /*Reset selection*/
    form.reset();
});

