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
});


// accept instructions from IRC chat bot via sockets

var io = require('socket.io').listen(54321);

// see http://stackoverflow.com/questions/6692908/formatting-messages-to-send-to-socket-io-node-js-server-from-python-client and https://gist.github.com/mattgorecki/1375505
io.sockets.on('connection', function (socket) {
  socket.on('pyevent', function(data) {
	console.log('pyevent' + data);
  });
  socket.on('movesphero', function(direction) {
        if(acceptingInput) {
			console.log('Moving Sphero in direction: '+direction);
			
			var newHeading = 0; 
			switch (direction) {
			  case 'LEFT':
				newHeading = 270;
				break;
			  case 'RIGHT':
				newHeading = 90;
				break;
			  case 'UP':
				newHeading = 0;
				break;
			  case 'DOWN':
				newHeading = 180;
				break;
			}
			relativeHeading = newHeading - prevHeading; // persisting on our own in prevHeading, since not sure if sphero.heading persists the previous heading
			if(relativeHeading < 0) {
				relativeHeading += 360; // heading must be between 0 and 365
			}
			
			var speed = 128;
			s.heading = relativeHeading;
			s.roll(speed, relativeHeading, 1);
			
			// stop sphero after 2 seconds
			setTimeout(function() {
				s.roll(0,s.heading||0,0);
			}, 2000);
			
		}
  });
});

connect(); // initiate first connection