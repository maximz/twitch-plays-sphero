"Twitch Plays" for Sphero
===================

"Twitch Plays Pokemon" for the physical world. The goal is to successfully guide a ball through a real-life maze. Type to control the ball's direction, and participate in Democracy or Anarchy modes. A fun twist on a classic game, merging virtual and physical realities.

Built at HackPrinceton Spring 2014. Special thanks to Walker Davis for the great maze and for figuring out the Sphero with me, and to Shubhro Saha for his client design.

### Running the game

#### To run:

```
node controller/app.js & 	#  launches node server that sends Bluetooth commands to Sphero and accepts new headings via websockets from the Python chatbot
source server/venv/Scripts/activate		# open virtualenv
python server/serve.py 		# launch IRC chatbot
```

Then navigate to http://twitchplayssphero.herokuapp.com and send chat commands "up", "down", "left", or "right". I suggest first connecting to your Sphero with the official iPhone or Android app and calibrating it (moving the blue tail light to point towards you), so that maze directions correlate with chat commands.

Alternate link for the web client: http://rollwithfriends.com.

#### To set up:

 * In the `controller` directory, you'll need to install `node-serialport` and `spheron` via npm
 * In the `server` directory, run `pip install -r requirements.txt` from within your virtualenv
 * Deploy the heroku directory under `client` to heroku.


### Architecture, design

**Overview:**

The webpage embed an IRC chat client (probably Slashnet's default webclient). Then we have a "Twitch Plays" bot sitting in that IRC chat room, and it aggregates user input. The aggregate input is sent to the "controller", which wraps it in a packet the Sphero can understand and sends it over Bluetooth the the paired Sphero.

When a user opens the page, the embedded chat client prompts for a username, and then they are ready to chat and control the Sphero.

We need a way for the client page to also display your current influence score/ranking, or maybe have a leaderboard. Maybe also have a real-time diagram or camera feed to see where the Sphero is in the maze.


**Democracy control:**

We will have an influence algorithm:

 # Collect all inputs over input time T
 # Find most common input -- weigh by current influence of each voter
 # Increase influence rank of those who voted for the chosen input. (Reset everyone else's influence?)

Influence means that those who vote with the hivemind often have more control, so they can eventually start trolling the group.

**Controls:**
 * Move X units in Y direction
 * Move indefinitely in a direction
 * Spin in place
 * Return to start of maze -- hard to implement, but would be perfect for high-influence trolling. Maybe limit voting for this function to those who pass a min influence threshold
 * No tricks for now, too hard to implement
 

### Code organization

 * **`controller/`:** A controller (running node, using node-serialport for BT connection and spheron) that sends motion commands to the Sphero.
 * **`server/`:** Python IRC chatbot (based on TwitchPlays) that aggregates user input and sends it to the Controller. Also computes influence.
 * **`client/`:** Front-end with embedded IRC client.

