document.addEventListener('DOMContentLoaded', function() {
    var checkPageButton = document.getElementById('clickIt');
    checkPageButton.addEventListener('click', function() {
      const Http = new XMLHttpRequest();
      const url='https://jsonplaceholder.typicode.com/posts';
      Http.open("GET", url);
      Http.send();

      Http.onreadystatechange = (e) => {
        console.log(Http.responseText)
}
      chrome.tabs.getSelected(null, function(tab) {
        alert("Current Url: " + tab.url);
      });
      
    }, false);
  }, false);