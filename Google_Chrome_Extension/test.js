document.addEventListener("DOMContentLoaded", function() {
  var request_to_twisted = new XMLHttpRequest();
  var current_url;
  chrome.tabs.query({'active': true, 'lastFocusedWindow': true}, function (tabs) {
      current_url = tabs[0].url;
  });
  var loader = document.getElementById('container2');

document.getElementById('t').addEventListener('click', function(){
loader.style.display="block";
request_to_twisted.open("GET", "http://localhost:16000?t="+current_url);
  request_to_twisted.onload = function() {
      if (request_to_twisted.status != 200) {
          console.log('No connection could be made');
      }
      else {
          loader.style.display="none";
chrome.tabs.create({"url": "file:///C:/Users/Tarkuen/Python-Projects/Hovedopgave/MVCHovedopgave/Google_Chrome_Extension/response.html"+"?"+request_to_twisted.responseText}, function(tab) 
{ });}}
request_to_twisted.send("COMMIT"); })
});