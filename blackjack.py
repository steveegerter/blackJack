import numpy as np
import sys
import pandas as pd

import deck
from deck import Cards, Deck
from roboPlayer import BlackjackDealer
from roboPlayer import autonomousPlayer

class hand:
        def __init__(self,deck,dealer):
                self.score = 0
                self.deck = deck
                if deck != None:
                    self.cards = [self.deck.popCard(), self.deck.popCard()]        
        def hit(self):
            score = self.get_score()
            if(len(self.cards)<5) and score <= 21:
                self.cards.append(self.deck.popCard())
            return score
        def get_score(self):
            points =  {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7,'8':8, '9':9, '10':10, 'J':10, 'Q':10, 'K':10}
            score = 0
            for card in self.cards:
                print(card)
                score = score+ list(card.values())[0]
            return score
                
        def summary(self,isDealer, isFinal):
               # print('summary for this hand\n')
                first = True
                for card in self.cards:
                     for key in card.keys():
                        if(first == True) and (isDealer == True) and (isFinal == False):
                           print('hole card')                           
                        else:
                           print(key)
                        first = False
                           
                points =  {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7,'8':8, '9':9, '10':10, 'J':10, 'Q':10, 'K':10}
                self.score = 0
                for card in self.cards:
                    for value in card.values():
                        if value == 'ace':
                           value = 1
                        self.score = self.score + value
                        #print('card value is', value)#score = score + card.get()
                if self.score > 21:
                     self.score = -1
                if (isDealer == True and isFinal == True) or isDealer == False:        
                    print('total score is ', self.score)
	
class player:
    def __init__(self,name,dealer,initial_cash):
        self.name = name
        self.money = initial_cash
        self.isDealer = dealer
        self.hand = None
        self.active = True
        #self.cards = []
  #  def setHand(hand):
        #self.hand = hand
  #  def turn(self):
       # self.hand.summary()
       # print('taking another card')
       # self.hand.hit()
       # self.hand.summary(self.dealer,False)
       # if self.hand.score > 21 or self.hand.score <= 0:
       #     print(self.name,'bust!')
       #     self.hand.score = 0
       #     return self.hand.score
       # if len(self.hand.cards) == 5:
       #     print('5 card under, you win!')
       #     return self.hand.score
    
                     
 
    def play(self):
        print('player name', self.name)
        #print('is this the dealer?',self.isDealer)
        result = self.turn()
        return result 
       # if(self.dealer == True):
       #    self.dealer_turn()
       # else:
       #     self.player_turn()
    def ante(self,amount):
        if self.money >= amount:
            self.money = self.money - amount
            return amount
        else:
            return 0
class Dealer(player):
      def __init__(self,name, isDealer, cash):
          player.__init__(self,name,isDealer,cash)
          
          pass
      def make_dealer_analysis_table(self, other_player_hand):
          hand = []
          for card in other_player_hand:
            for value in card.values():
                hand.append(value)
          for i in range(len(hand),5):
              hand.append(0)
          for card in self.hand.cards:
              for value in card.values():
                   hand.append(value)
          for i in range(len(hand),10):
              hand.append(0)
#          cards = np.array([hand])
          return hand
          
      def turn(self):
      #def dealer_turn(self):
        results = ["empty","dealer wins", "player wins", "dealer busts", "player busts", "push"]
        print("dealer's turn")
        players = [player1,autoPlayer]
        #list of dictionaries
        hands = []
        for player in players:
             hands.append(self.make_dealer_analysis_table(player.hand.cards))
        #print('dealer sees the high hand is', player1.hand.cards)
      #  print('dealer analysis tables:', hands)
        
        
        #while dealer.hand.score < player1.hand.score: 
        #    score = self.turn()
        #    print('dealer scores', score)
        #    if score == -1 or score == 21 or len(self.hand.cards) == 5:
        #         break   
        dealerai = BlackjackDealer()
        #cards = np.array([[high_hand.values(),self.hand.cards.values()]])
        #print('dealer uses following for prediction',cards)
        count = 0
        for card_predict in dealerai.dealer_cards:
             for hand in hands:
                 #if self.hand.score >= 21:
                 #    break
                 print('hand to analyze is', hand)
                 result = dealerai.dealer_result_classifier.predict(np.array([hand]))
                 print('result of the hand so far looks like', results[int(result)])
                 if(int(result) ==3): # dealer busts
                    break
                 result = 0
                 prediction = card_predict.predict(np.array([hand]))
                 print('dealer predicts',prediction)
                 if(prediction > 1.0):
                     self.hand.hit()
                     print("dealer's hand:",self.hand.cards)
                     if (len(self.hand.cards)) >= count +2:
                         
                         add_card = list(self.hand.cards[2+count].keys())[0]
                         add_card_value = self.hand.cards[2+count][add_card]
                         hand[7+count] = add_card_value
                         #print("add a card to the dealer's hand, value: ", add_card_value)
                     else:
                         pass
                     count = count + 1
                     #cards = np.array([hand])
                     break
                     #print('count is', count,'card table :',cards)
             print('dealer now holds', self.hand.cards)
        for hand in hands:
             result = dealerai.dealer_result_classifier.predict(np.array([hand]))
             #print('result for hand', results[int(result)])
             # now try to work out the amount to payy
             two_card_sum = sum(hand[0:1])
             sumofcards = sum(hand[0:4])
             blkjck = 1 if two_card_sum == 21 else 0
             #print('sumof deal is',list(self.hand.cards.values())[0])
             #dealer_vals = [list(x.values())[0] for x in self.hand.cards ]
             dealer_vals = sum(hand[5:9])
             print('dealer vals:', dealer_vals)
             sumofdeal = dealer_vals #sum(dealer_vals)
             payout_data = [two_card_sum,int(result),sumofcards,blkjck,sumofdeal]
             payamt = dealerai.dealer_payout.predict(np.array([payout_data]))
             #print('payout data for this hand is',payout_data)
             print('result for hand', results[int(result)],'dealer pays this player', int(payamt))
                 
class HumanPlayer(player):
      def __init__(self,name, isDealer, cash):
          player.__init__(self,name,isDealer,cash)
          
      def turn(self):
       # self.hand.hit()
        if self.hand.score >= 21 or self.hand.score < 0:
           return False
        choice = input('(h)it, (s)tand or (d)doubledown?\n')   
        if choice=='h':
           # dealer should really be in control of whether the player gets another card or not
           self.hand.hit() 
           self.hand.summary(self.isDealer,False)
           return True
           # could this be a lambda function?
           #score = #self.turn()
           #if self.hand.score == 0 or self.hand.score >= 21 or len(self.hand.cards) == 5:
           #    break  
        else:
           return False   

class NonHumanPlayer(player):
      def __init__(self,name, isDealer, cash):
           player.__init__(self,name,isDealer,cash)
           self.card_table = []
      def turn(self):
           autoPlayer = autonomousPlayer()
           
          # print(self.name,':examining cards', self.hand.cards, dealer.hand.cards)
           if len(self.card_table) == 0:
              for card in self.hand.cards:
                 for value in card.values():
                    self.card_table.append(value)
              for i in range(len(self.card_table),5):
                 self.card_table.append(0)
             # print('card table so far', self.card_table)
             # print("dealer's hand:", dealer.hand)
              dealer_shows_card = list(dealer.hand.cards[0].values() )[0]
              self.card_table.append(dealer_shows_card)
             # print('dealer is showing',self.card_table[:5])
           cards = np.array([self.card_table])
           #print('cards used for prediction:', cards)
           count = 0
           for value in self.hand.cards:
                if value ==0:
                   break
                count = count + 1
    #       for card_predict in autoPlayer.player_cards:
           prediction = autoPlayer.player_cards[count - 2].predict(cards)
           #print('auto player predicts',prediction)
           if(prediction > 1.0):
                 self.hand.hit()
                 #add_card = list(self.hand.cards[2+count].keys())[0]
                 #add_card_value = self.hand.cards[2+count][add_card]
                 #card_table[2+count] = add_card_value
                 #print("add a card to the dealer's hand, value: ", add_card_value)
                 #count = count + 1
                 #cards = np.array([card_table])
                 self.hand.summary(False,False)
                 return True
           else:
                 print('autoplayer finishes with', self.hand.cards)
                 return False

def blackJackHand(players,  ante_amount):
    # Driver Code
    # Creating objects
    objCards = Cards()
    objDeck = Deck()
    kitty = 0

    print('\v-----------------------------------------\n')
    print(len(players),'players including the dealer')
    objShuffleCards = deck.ShuffleCards()
    objShuffleCards.shuffle()
    player = 0
    for player in players:
        if player.ante(ante_amount) == ante_amount:
           player.hand = hand(objShuffleCards, False)
           print('===========\n',player.name,'\n===========\n')
           player.hand.summary(player.isDealer,False)
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
    #card_table.insert(0,'dealer cards',dealer.hand.cards)
   # card_table = card_table + pd.DataFrame.from_dict(dealer.hand.cards)
    while players[0].active == True or players[1] == True:
        for player in players:
            #print('===========\n',player.name,'\n===========\n')
            # player.hand.summary(player.dealer, True)
            #card_table_as_dict = {'player1':player1.hand.cards, 'dealer':dealer.hand.cards}       
            #card_table = pd.DataFrame(card_table_as_dict)
            #print(card_table)
            if(player.active == True):
                player.active = player.play()
                if len(player.hand.cards) == 5:
                    break
            else:
               print(player.name,'is finished')
        player = 0
    print('player1 :', player1.active, 'autoPlayer', autoPlayer.active)      
    dealer.play()
    #dealer = players[-1]       
    print('===========\n',dealer.name,'\n===========\n')
    dealer.hand.summary(True,True)
    # this section should probably be moved to the dealer_turn functions
    print('autoPlayer scores', autoPlayer.hand.score)
    if player1.hand.score > dealer.hand.score or len(player1.hand.cards) == 5 or dealer.hand.score == -1 or dealer.hand.score > 21:
        print('Player1 wins with a score of', player1.hand.score)
        print('house scored', dealer.hand.score)
        player1.money = player1.money +kitty
        kitty = 0
    else:
        print('House wins with a score of ', dealer.hand.score)
        print('player1 score was', player1.hand.score)
    print('player1 balance now ', player1.money)
    dealer.hand.cards = []
    for player in players:
        player.hand.cards = []
        player.active = True
    
   
##########################################################################   
#def blackjack():
if(len(sys.argv)==2):
   ante_amt =   sys.argv[1]
else:
   ante_amt = "10"
print('********************************************************************')
print('                         BlackJack')
print('                         $',ante_amt,' to play')
print('********************************************************************')
dealer = Dealer("Alice",True,10000)
#Alice = dealer()
player1 = HumanPlayer("player1", False,100)
autoPlayer = NonHumanPlayer("autoPlayer",False,100)

while input('play a(nother) hand?') == 'y':
    blackJackHand([player1,autoPlayer], int(ante_amt) )
print('Bye for now')
