window.addEventListener('load', smartMeter);
function smartMeter() {
  function getAPIData() {
    var http = new XMLHttpRequest();

    http.onreadystatechange = function() {
        if(this.readyState === 4 && this.status === 200) {
          update(JSON.parse(this.responseText));
        }
    }
   
    http.open("GET", "/api", true);
    http.send();
  }
 
 
  function update(apiData) {
    
    
    var tC     = document.getElementById("tC");
    var tF     = document.getElementById("tF");
    var pP     = document.getElementById("pP");
    var pM     = document.getElementById("pM");
    var h      = document.getElementById("h"); 
    
   
    tC.innerHTML  = parseFloat(apiData.temp.tC).toFixed(2) + "°C";     
    tF.innerHTML  = parseFloat(apiData.temp.tF).toFixed(2) + "°F";     
    pP.innerHTML  = parseFloat(apiData.pres.pP).toFixed(2) + " pP";    	
    pM.innerHTML  = parseFloat(apiData.pres.pM).toFixed(2) + " pM";    
    h.innerHTML   = parseFloat(apiData.hum).toFixed(2) + " %";     
    	
    
  }

  function app() {
    window.setInterval(function() {
      getAPIData();
    }, 5000);
  }
  app();
}