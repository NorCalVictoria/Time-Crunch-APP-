$(document).ready(function() {

  $("#search").click(function() { // click event for search button
    let searchReq = $.get("/sendRequest/" + $("#query").val());  // SEND SEND SEND building url send request (api google places)takes in query and gets send request
    searchReq.done(function(data) {
  console.log('GOT HERE', data);
      $("#url").attr("href", data.result);   // once get request complete it will add result to link
       //$("#image").html(data); 
    });
  });

});
 