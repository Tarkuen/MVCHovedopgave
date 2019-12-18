
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
        chrome.tabs.create({'url': "C:/Users/Tarkuen/Python Projects/Hovedopgave/MVCHovedopgave/vof_plugin/response.html"+'?'+request_to_twisted.responseText}, function(tab) {
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
        chrome.tabs.create({'url': "C:/Users/Tarkuen/Python Projects/Hovedopgave/chrome_plugin/testplugin/response.html"+'?'+request_to_twisted.responseText}, function(tab) {
        });
      }
    }
    console.log(current_url)
    request_to_twisted.send("COMMIT");
    
  })

  // document.getElementById('scan_key').addEventListener('click', function(){
  //   console.log('scan key')
  //   loader.style.display="block";
  //   var target = document.getElementById('keyinput')
  //   request_to_twisted.open('GET', "http://localhost:16000?target="+target.innerHTML+"&url="+current_url);
  //   request_to_twisted.onload = function() {
  //     if (request_to_twisted.status != 200) {
  //       console.log('No connection could be made');
  //     }
  //     else {
  //       loader.style.display="none";
  //       chrome.tabs.create({'url': "C:/Users/Tarkuen/Python Projects/Hovedopgave/chrome_plugin/testplugin/response.html"+'?'+request_to_twisted.responseText}, function(tab) {
  //       });
  //     }
  //   }
  //   console.log(current_url)
  //   request_to_twisted.send("COMMIT");

  // })


}, false);
