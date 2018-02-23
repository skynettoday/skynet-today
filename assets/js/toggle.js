var displayingCategorical = true;
$(function() {
    var form = document.querySelector("#writingToggleForm");
    form.addEventListener("change", function(event) {
        console.log("Toggling writing display!");
        if(displayingCategorical){
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
        displayingCategorical = !displayingCategorical;
    });
    $("#editorials").fadeOut();

    /*Reset selection*/
    form.reset();
});

