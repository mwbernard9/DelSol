var outputValue1 = 0;
var lastOutputValue1 = -1;
var outputValue2 = 0;
var lastOutputValue2 = -1;
var adafruitUsername = 'mbernard';
var adafruitFeed = 'altitude';
var adafruitFeed2 = 'azimuth';
var adafruitFeed3 = 'light';
var adafruitAioKey = '3d053bf413d54b4b99b66b2d53b50e6d';


//lightLevel Reader
setInterval(function(){
    getAdaIO(adafruitUsername, adafruitFeed3, adafruitAioKey, changeBar);
}, 2000);

function changeBar(data) {
    var dataNum = parseInt(data/45);
    $("#amount3").text(dataNum + "%");
    $("#lightlevel").width(data/6.5);

}

//altitude
setInterval(function(){
    // send value periodically, if changed
    if (outputValue1 != lastOutputValue1) {
      setAdaIO(adafruitUsername, adafruitFeed, adafruitAioKey, outputValue1);
      lastOutputValue1 = outputValue1;
    }
}, 2000);

//azimuth
setInterval(function(){
    // send value periodically, if changed
    if (outputValue2 != lastOutputValue2) {
      setAdaIO(adafruitUsername, adafruitFeed2, adafruitAioKey, outputValue2);
      lastOutputValue2 = outputValue2;
    }
}, 2000);

//display alt and az
$(document).ready(function(){
    $( "#output1" ).on("change mousemove", function() {
        outputValue1 = this.value;
        $("#amount1").text(outputValue1);
    });
    $( "#output2" ).on("change mousemove", function() {
        outputValue2 = this.value;
        $("#amount2").text(outputValue2);
    });
});
