$(function(){
  $("#submit_game").bind('click', function(e){
    e.preventDefault();
    alert('test');

    $.ajax({
      type: "POST",
      url: "/start_computation",
      data: $('#wikiGameForm').serialize(),
      // data: {
      // 	start_page: ("#start_page").val(),
      // 	end_page: ("#end_page").val(),
      // 	max_turns: ("#max_turns").val()
      // },
      success: function(data){
        try {
          if (data['errors'] != false){
            if (data['errors'] == True){
              alert("There was an unknown error.")
            } else if (data['errors'].length == 1) {
              alert(data['errors'][0] + " is not a valid Wikipedia page name.")
            } else {
              alert(data['errors'][0] + " and " + data['errors'][1] " are not a valid Wikipedia page names.")
            }
          } else {
            break;
          }
        } catch (err) {
          alert("There was an unknown error: " + err);
        }

      },
      error: function(data){
        alert("ERROR: " + str(data));
      }
    });
  });
});
