# Tractorbus Online
An online multiplayer client for playing the card game [Tractor](https://www.pagat.com/kt5/tractor.html). Visit http://tractor39.herokuapp.com/ to try it out yourself! (It might take a few seconds to load).
## Game Logic
Backend code was written in collaboration with Andrew Zhang, Adam Zheng, and Raymond Li. A version of the game built with Pygame can be found at https://github.com/adamczheng/tractor-client. All game logic was written using Python.
## GUI
Frontend code was done with Javascript and basic CSS. The user interface was inspired by Henry Charlesworth's Big 2 client (https://github.com/henrycharlesworth/big2_PPOalgorithm). Flask-SocketIO was used for networking to handle user inputs and synchronize multiplayer gameplay.
##Gameplay
---
**Note**
Four players must be on the website http://tractor39.herokuapp.com/ to start a game.
In this demo, we have four unique players on each tab.
---
We can select and play a card by clicking on the sprite. Here, our player wants to play 10 &spadesuit; .
![Playing a single card](https://gyazo.com/4ba789c89a3381e8d88853df8801bff9)
The red dot moves to the player with the biggest card, which is the person that played the largest card.
![Last player moves](https://gyazo.com/645bb212bb803ad87bd5538ec1e8dc4f)
If the attacking side (Tabs 2 and 4) win the round, the appropriate amount of points are added to the attacker points.
![Image from Gyazo](https://gyazo.com/c9f1337dafc22faf652fa11e0f566d1b) 
The game supports different types of plays such as Pairs,  and Tractors (shown below)
![Image from Gyazo](https://gyazo.com/0de0bbcd0b21d3924731c55dfbd8665d)
You can take back your move if the next player has not made their move yet.
![Image from Gyazo](https://gyazo.com/8cfd648374d33cd80e82055dc6fe3b57)
You can also clear your selection and play a different hand conveniently with the clear button.
![Image from Gyazo](https://gyazo.com/a72bd86ddebf5810333a23a3ef9f854d)
