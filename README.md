# BlackJack
##Intro
This is an AI/ML-based Blackjack game. A full description will be published shortly.

##Description
This game is currently console-based since the point of the project was to gain some more practical experience with TensorFlow, which the project is based on.
The dealer attempts to follow the rules of Blackjack as closely as possible. The main object used for AI/ML predictions is called card_predicter although it is used for than simply deciding whether to draw another card or not. In BlackJack, an ace can take the value 1 or 11, depending on the player's choice. For this reason, a prediction model is used to determine whether to promote the ace or not. This game also includes a number of robot players. The models used for the non-dealer robot players is slightly different since the non-dealer players can only see one of the dealer's two cards while they determine how many cards to draw. Conversely, the dealer who plays last, can see all of the player's cards. Hence, the data sets used are slightly different.

##Models
The dataset used for this project comes from https://www.kaggle.com/mojocolors/900000-hands-of-blackjack-results
