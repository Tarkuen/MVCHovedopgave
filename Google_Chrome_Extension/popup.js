
document.addEventListener("DOMContentLoaded", function() {

  var request_to_twisted = new XMLHttpRequest();
  var current_url;
  chrome.tabs.query({'active': true, 'lastFocusedWindow': true}, function (tabs) {
    current_url = tabs[0].url;
  });

  var loader = document.getElementById('container2');

  document.getElementById('scan_one').addEventListener('click', function(){
    console.log('scan one')
    loader.style.display="block";
    request_to_twisted.open('GET', "http://localhost:16000?target="+current_url);
    request_to_twisted.onload = function() {
      if (request_to_twisted.status != 200) {
        console.log('No connection could be made');
      }
      else {
        loader.style.display="none";
        chrome.tabs.create({'url': "file:///C:/Users/Tarkuen/Python%20Projects/Hovedopgave/chrome_plugin/testplugin/response.html"+'?'+decodeURI(request_to_twisted.responseText)}, function(tab) {
        });
      }
    }
    console.log(current_url)
    request_to_twisted.send("COMMIT");
  })
  
  document.getElementById('scan_all').addEventListener('click', function(){
    console.log('scan all')
    loader.style.display="block";
    request_to_twisted.open('GET', "http://localhost:16000?root="+current_url);
    request_to_twisted.onload = function() {
      if (request_to_twisted.status != 200) {
        console.log('No connection could be made');
      }
      else {
        loader.style.display="none";
        chrome.tabs.create({'url': "file:///C:/Users/Tarkuen/Python%20Projects/Hovedopgave/chrome_plugin/testplugin/response.html"+'?'+request_to_twisted.responseText}, function(tab) {
        });
      }
    }
    console.log(current_url)
    request_to_twisted.send("COMMIT");
    
  })
});

// var img_topdom = String(Math.floor(Math.random() * 100))
// var elem = document.getElementById('uniqueId');
// red = Math.floor(Math.random()*255)
// green = Math.floor(Math.random()*255)
// blue = Math.floor(Math.random()*255)
// var colourstring = 'rgb('+red+', '+green+', '+blue+')'
// elem.style.backgroundColor = colourstring
// elem.style.height ='50px'
// elem.style.width = '50px'

