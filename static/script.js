$(document).ready(function() {

  $("#search").click(function() { // click event for search button
    var searchReq = $.get("/sendRequest/" + $("#query").val());  // SEND SEND SEND building url send request (api google places)takes in query and gets send request
    searchReq.done(function(data) {
      $("#url").attr("href", data.result);   // once get request complete it will add result to link
    });
  });

});
 