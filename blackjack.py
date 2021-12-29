import numpy as np
import sys
import pandas as pd

import deck
from deck import Cards, Deck
from roboPlayer import BlackjackDealer
from roboPlayer import autonomousPlayer
import player
from player import NonHumanPlayer
from player import hand

def print_card_table(isFinal):
    card_table_dict = {dealer.name:[]}
    card_labels = []
    if(isFinal == True):
       card_labels = [list(label.keys())[0] for label in dealer.hand.cards]
    else:
       card_labels = [list(dealer.hand.cards[0].keys())[0]]
       card_labels.append( {'facedown',0} )
    for x in range(len(card_labels),5):
        card_labels.append('joker'+str(x))
    values = [list(card.values())[0] for card in dealer.hand.cards]
    if isFinal == True:
       card_labels.append(sum(values))
    else:
       card_labels.append('?')
    card_table_dict = {dealer.name:card_labels}
    for player in players:
        hand = [list(card.keys())[0] for card in player.hand.cards]
        for x in range(len(hand),5):
              hand.append('joker'+str(x))
        values = [list(card.values())[0] for card in player.hand.cards]
        hand.append(sum(values))
        card_table_dict[player.name] = hand
        
    #card_labels = [list(label.keys())[0] for label in dealer.hand.cards]
    #print(card_table_dict)
    print('card table\n----------------------\n')
    print(pd.DataFrame.from_dict(card_table_dict))
    
def blackJackHand(players,  ante_amount):
    # Driver Code
    # Creating objects
    objCards = Cards()
    objDeck = Deck()
    kitty = 0
    print('\v-----------------------------------------\n')
    print(len(players),'players not including the dealer')
    objShuffleCards = deck.ShuffleCards()
    objShuffleCards.shuffle()
    player = 0
    for player in players:
        if player.ante(ante_amount) == ante_amount:
           player.hand = hand(objShuffleCards, False)
           #print('===========\n',player.name,'\n===========\n')
           player.hand.summary(player.isDealer,False)
           #print('================================\n')
           kitty = kitty + ante_amount
        else:
           print('player:',player.name,'is broke')
           pass
    if dealer.ante(ante_amount) == ante_amount:
           dealer.hand = hand(objShuffleCards, False)
           print('===========\n',player.name,'\n===========\n')
           kitty = kitty + ante_amount
    else:
           print('player:',player.name,'is broke')
           pass
    
           
    print('dealer shows', list(dealer.hand.cards[0].keys())[0])
    print_card_table(False)
            
    while players[0].active == True or players[1].active == True:
        for player in players:
            if(player.active == True):
                dealer_show_card = list(dealer.hand.cards[0].values())[0]
                player.active = player.play(dealer_show_card,None)
                if len(player.hand.cards) == 5:
                    break
            else:
               print(player.name,'is finished')
        print_card_table(False)
        player = 0
    #print('player1 :', player1.active, 'autoPlayer', autoPlayer.active)      
    dealer.play(None,players)
    #dealer = players[-1]       
    print('===========\n',dealer.name,'\n===========\n')
    dealer.hand.summary(True,True)
    print_card_table(True)
    print(dealer.name, 'total',dealer.hand.score)
    dealer.hand.cards = []
        
    for player in players:
        #print(player.name, 'total',player.hand.score)
        player.hand.cards = []
        player.active = True
        print('player ', player.name, 'now has', player.money)
    
   
##########################################################################   
#def blackjack():
nRobotPlayers = 0
#autoPlayer1 = NonHumanPlayer("autoPlayer1",False,100)
ante_amt = "10"
auto_players = []
Thresholds = [33, 25, 0 , 50]
if(len(sys.argv)>1):
   for i in range(1,len(sys.argv)):
      if sys.argv[i].find('ante') != -1:
          ante_amt =   sys.argv[i][5:]
      elif sys.argv[i].find('auto_players') != -1:
          num = int(sys.argv[i][13:])
          auto_players = [NonHumanPlayer(name='auto_player'+str(n),threshold=Thresholds[n]) for n in range(num)]
  
print('********************************************************************')
print('                         BlackJack')
print('                         $',ante_amt,' to play')
print('********************************************************************')
dealer = player.Dealer(name="Alice(Dealer)")
player1 = player.HumanPlayer(name="player1", cash=100)
players = [player1]
players.extend(auto_players)
#print('players are', players)
while True:
    answer = input('play a(nother) hand?') 
    if answer == 'q':
        break
    blackJackHand(players, int(ante_amt) )
print('Bye for now')
