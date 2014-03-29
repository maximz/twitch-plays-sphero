/* jshint node:true */
/*

 Run this file with node app.js, after pairing with the Sphero.
 Accepts movement directions, then converts them to Sphero language and sends them out over Bluetooth.

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
  setTimeout(connect, 1000); // reconnect in 1000 ms
});

var acceptingInput = false;
var prevHeading = 0;

s.on('open', function() {
	console.log('Sphero connected');
	acceptingInput = true;
	/*s.roll(128, 270, 1);
	setTimeout(function() {
		s.heading=180; // doesn't do anything
	}, 500);*/
	
});


// accept instructions from IRC chat bot

var io = require('socket.io').listen(54321);

// see http://stackoverflow.com/questions/6692908/formatting-messages-to-send-to-socket-io-node-js-server-from-python-client and https://gist.github.com/mattgorecki/1375505
io.sockets.on('connection', function (socket) {
  socket.on('pyevent', function(data) {
	console.log('pyevent' + data);
  });
  socket.on('movesphero', function(data) {
        if(acceptingInput) {
			console.log('Moving Sphero with following command: '+data);
			newHeading = parseInt(data) - prevHeading;
			if(newHeading<0) {
				newHeading += 360;
			}
			var speed = 128;
			s.roll(speed, newHeading, 1);
		}
  });
});

connect(); // initiate first connection