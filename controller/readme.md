### Installation

The crucial part is getting https://github.com/voodootikigod/node-serialport working.
Follow those instructions; I used the VS2013 x64 native tools command prompt (didn't try other vs2013 ones).

To evaluate the different node + sphero libraries, I ran:

	npm install serialport -g		success
	npm install sphero -g 			success
	npm install spheron -g			success
	npm install node-sphero -g 		failed



All `npm install` calls happen through the VS2013 command prompt.

In local directory:

 # `npm install serialport` 
 # `npm install spheron` (maybe previous line is unnecessary)
 # Pair laptop with Sphero via Bluetooth settings. Then go into bluetooth settings and find out which COM Port is being used.
 # Run `node listports.js` to confirm the COM Port information as interpreted by node-serialport.
 # Then run the below sample code:

```
var spheron = require('spheron');
var sphero = spheron.sphero();
var spheroPort = 'COM10';
var COLORS = spheron.toolbelt.COLORS;

sphero.on('open', function() {
  sphero.setRGB(COLORS.BLUE, false);
});

sphero.open(spheroPort);
```

And it works! Now run `node app.js` for the main police-siren-lights test and the roll test.

(BTW, I tried to get the `npm install sphero` library to work with this code, but it didn't communicate with our Sphero:)

```
var sphero = require('sphero');

var client = sphero.createClient();
client.connect(function () {
  client.color('red');
});
```
