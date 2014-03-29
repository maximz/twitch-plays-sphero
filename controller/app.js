/* jshint node:true */
/*

 Flash blue and red like a police siren

 This file is expected to be run something like this:

 $ node examples/repl.js
 S> .load examples/vege.js
 S> police(100, 500);
 S> repeat = true;
 S> police(100,500);
 S> repeat = false;

 */
var spheron = require('spheron');
//var sphero = spheron.sphero();

var o = { resetTimeout:true, requestAcknowledgement:true };
var s = spheron.sphero().resetTimeout(true).requestAcknowledgement(true);

s.on('error', function(error) {
  console.log('Sphero error:', error);
});

s.on('open', function() {

  console.log('Sphero connected');
  police(100,500);
  //repeat=true;
  
  //s.roll(128)
s.heading = 270;
s.roll(128, 270, 1);
  
  /*
  var colourStart = 0x006600;
var colourStop = 0x00FF00;
  
    s.write(spheron.commands.api.setStabalisation(false));

  var step = 0;
  var steps = 30*1;

  function nextColour() {
    var colour = toolbelt.colorStop(colourStart, colourStop, (Math.sin(step/steps)+1)/2);
    s.write(spheron.commands.api.setRGB(colour, false, { resetTimeout:true}));
    step++;
    setTimeout(nextColour, 16);
  }

  nextColour();*/


});

//s.open(dev);
//var spheroPort = 'COM10';
//sphero.open(spheroPort);
s.open('COM10');


var repeat = false;

var police = function(delay1, delay2) {
  s.setRGB(0x000000, false);
  setTimeout(function() {
    s.setRGB(0x0000FF);
  }, delay1);
  setTimeout(function() {
    s.setRGB(0x000000, false);
  }, delay1*2);
  setTimeout(function() {
    s.setRGB(0x0000FF, false);
  }, delay1*3);
  setTimeout(function() {
    s.setRGB(0x000000, false);
  }, delay1*4);

  setTimeout(function() {
    s.setRGB(0xFF0000, false);
  }, delay1*5);
  setTimeout(function() {
    s.setRGB(0x000000, false);
  }, delay1*6);
  setTimeout(function() {
    s.setRGB(0xFF0000, false);
  }, delay1*7);
  setTimeout(function() {
    s.setRGB(0x000000, false);
  }, delay1*8);

  if (repeat) {
    setTimeout(function() {
      police(delay1, delay2);
    }, delay2+delay1*8);
  }
};
