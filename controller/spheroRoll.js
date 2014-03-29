/* jshint node:true */
/*

 Simple roll tests.
 */
var spheroPort = 'COM10'; // set this port properly!
var spheron = require('spheron');

var o = { resetTimeout:true, requestAcknowledgement:true };
var s = spheron.sphero().resetTimeout(true).requestAcknowledgement(true);

var connect = function() { 
	// attempt to connect to Sphero
	console.log('trying to connect');
	s.open(spheroPort);
}

s.on('error', function(error) {
  console.log('Sphero error:', error);
  acceptingInput = false;
});

s.on('open', function() {
	console.log('Sphero connected');
	
	// see https://github.com/alchemycs/spheron/search?q=roll
	
	s.roll(128, 180, 1);
	setTimeout(function() {s.roll(128, 0, 10);}, 5000);
	//setTimeout(function() {s.roll2(128, 180, 5);}, 6000);

});

connect(); // initiate first connection