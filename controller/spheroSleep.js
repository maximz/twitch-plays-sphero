/* jshint node:true */
/*

 Puts sphero to sleep. Awaken with double-shake.
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
	
	console.log('Putting it into sleep mode');
	s.sleep(0,0,0);
	
	console.log('asleep');
});

connect(); // initiate first connection