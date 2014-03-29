twitch-plays-sphero
===================

"Twitch plays" for Sphero! HackPrinceton Spring 2014


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
