twitch-plays-sphero
===================

"Twitch plays" for Sphero! HackPrinceton Spring 2014


### Architecture and code organization

 * **`server/`:** A server (running node probably) that has open sockets to all "clients" (people who see sphero position and contribute movement requests) and an open socket to the "controller". Will sit on Heroku or somewhere similar. May also have a chatroom for all the "clients".
 * **`controller/`:** Sits on one of our machines and feeds Bluetooth commands to the Sphero. Unclear what language -- depends on SDK availability.
 * **`client/`:** Allows input via keyboard arrows and trick buttons, sent via websocket to server. Maybe will have a chatroom running. Can we back-infer position and display it to the "clients"? This is just front-end.
