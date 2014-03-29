/* jshint node:true */
/*

 Self levels -- i.e. hold Sphero with the side you want up, and then run this while holding.
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
	
	s.selfLevel(1,2,3,4);
	
	console.log('self leveled');
});

connect(); // initiate first connection