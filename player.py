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
                    #print('hand.__init__() initial cards are',self.cards)   
        def hit(self):
            score = self.get_score()
            if(len(self.cards)<5):# and score <= 21:
                self.cards.append(self.deck.popCard())
            return score
        def get_score(self):
            points =  {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7,'8':8, '9':9, '10':10, 'J':10, 'Q':10, 'K':10}
            score = 0
            for card in self.cards:
                #print('get_score():',card)
                score = score+ list(card.values())[0]
            return score
                
        def make_ace_11(self):
            print('print_ace_11(): looking for an ace in ', self.cards) 
            for acard in self.cards:
                key = list(acard.keys())[0]
                print('key value',key)
                if key.find('A ') != -1:
                   print('found an ace to promote at', acard[key])
                   acard[key] = 11
                   break
            print('hand is now', self.cards)
        def ace_promote(self,card_table,predicters):
           if card_table[0] == 1:
               print('use the following to decide to promote ace', np.array(card_table[1:2]))
               promote = predicters[0].predict(np.array(card_table[1:2]))
               print('checking promote ace value', abs(promote.item(0)))
               if abs(promote.item(0)) > 50.0:
                   print('promote ace to 11')
                   self.make_ace_11()
           
           if card_table[1] == 1:
               print('use the following to decide to promote ace', np.array(card_table[0:1]))
               promote = predicters[1].predict(np.array(card_table[0:1]))
               print('checking promote ace value', abs(promote.item(0)))
               if abs(promote.item(0)) > 50.0:
                   print('promote ace to 11')
                   self.make_ace_11()      
    
        def summary(self,isDealer, isFinal):
               # print('summary for this hand\n')
                first = True
                #cards = pd.DataFrame (self.cards)
                card_labels = [list(x.keys())[0] for x in self.cards]
                #print(card_labels)
                #for card in self.cards:
                #     for key in card.keys():
                #        if(first == True) and (isDealer == True) and (isFinal == False):
                #           print('hole card')                           
                #        else:
                #           print(key)
                #        first = False
                           
                points =  {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7,'8':8, '9':9, '10':10, 'J':10, 'Q':10, 'K':10}
                self.score = 0
                for card in self.cards:
                    for value in card.values():
                        if value == 'ace':
                           value = 1
                        #print('summary value in card.values()',value)
                        self.score = self.score + value
                        #print('card value is', value)#score = score + card.get()
               # if self.score > 21:
               #      self.score = -1
                if (isDealer == True and isFinal == True) or isDealer == False:        
                    #print('total score is ', self.score)
                    pass
	
class player:
    def __init__(self,name,dealer=False,initial_cash=100):
        self.name = name
        self.money = initial_cash
        self.isDealer = dealer
        self.hand = None
        self.active = True
        #self.cards = []             
 
    def play(self,dealer_cards,players):
        #print('=================================\n')
        #print('player name', self.name)
        #print('is this the dealer?',self.isDealer)
        result =         self.turn(dealer_cards, players)
        #print('=================================\n')
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
      def __init__(self,name="Dealer", cash=10000, threshold=50.0):
          player.__init__(self,name,True,cash)
          self.threshold=threshold
          pass
      def pad_player_hand(self, hand):
          for i in range(len(hand),5):
              key = 'joker'+ str(i)
              hand.append({key:0})
      def make_player_vs_dealer_hand(self, player):
          dealer_values = [list(x.values())[0] for x in self.hand.cards ] #+ [0 for i in range(len(self.hand.cards),3)]
          player_values = [list(x.values())[0] for x in player.hand.cards ]
          return player_values+dealer_values
      def turn(self,dealer_cards, players):
      #def dealer_turn(self):
        print("dealer's turn")
        #players = [player1,autoPlayer]
        #list of dictionaries
        hands = []
        for player in players:
             #hands.append(self.make_dealer_analysis_table(player.hand.cards))
             self.pad_player_hand(player.hand.cards)
        
        dealerai = BlackjackDealer()
        card_table = [list(x.values())[0] for x in self.hand.cards]
        self.hand.ace_promote(card_table,dealerai.ace_promote_predicters)
        #cards = np.array([[high_hand.values(),self.hand.cards.values()]])
        #print('dealer uses following for prediction',cards)
        count = 0
        for card_predict in dealerai.dealer_cards:
             for player in players:
                 hand = self.make_player_vs_dealer_hand(player)
                 #print('hand to analyze is', hand)
                 #print('hand',hand, card_predict.label)
                 
                 if len(hand) != (count +2+len(player.hand.cards)):
                     print('length of the card array is', len(hand), 'instead of', count +2+len(player.hand.cards))
                     self.hand.cards.append({'joker'+str(count):0})
                     print(self.hand.cards)
                     hand = self.make_player_vs_dealer_hand(player)
                     print('hand is now:',hand)
                 #print('about to predict on round', count, 'with', len(hand), 'cards')
                 #np_hand = np.array([hand])
                 prediction = card_predict.predict(np.array([hand]))
                 #print('dealer predicts',abs(prediction.item()),"% probability that taking another card is a good idea")
                 if(abs(prediction.item()) > self.threshold):
                     self.hand.hit()
                     hand.append(list(self.hand.cards[len(self.hand.cards) - 1].values())[0])
                     break
             hand2 = hand  + [0 for x in range(len(hand),10)]
             didIwin = dealerai.dealer_result_classifier.predict(np.array([hand2]))
             #print('argmax of dealer result classifier', np.argmax(didIwin))
             result_text = list(dealerai.game_results.keys())[np.argmax(didIwin)]
             #print(didIwin,result_text)
             #self.hand.cards.append({'joker'+str(count):0})
             count+=1
             if result_text == 'Dlwin' or result_text == 'Bust' or result_text=='PlBust':
                break
             
         # work out the results    
        for player in players:
             dealer_values = [list(x.values())[0] for x in self.hand.cards ]+ [0 for i in range(len(self.hand.cards),5)]
             player_values = [list(x.values())[0] for x in player.hand.cards ]
             hand = player_values+dealer_values
             #hand = self.make_player_vs_dealer_hand(player)
             for pad in range(len(hand),10):
                  hand.append(0)
             #print(hand)
             result_array = dealerai.dealer_result_classifier.predict(np.array([hand]))
             result_txt = list(dealerai.game_results.keys())[np.argmax(result_array)]
             # print('result for hand with', player.name, result_txt)
             # now try to work out the amount to payy
             two_card_sum = sum(hand[0:1])
             sumofcards = sum(hand[0:4])
             #blkjck = 1 if two_card_sum == 21 else 0
             sumofdeal = sum(hand[5:])
             #blkjck,
             payout_data = [two_card_sum,np.argmax(result_array),sumofcards,sumofdeal]
             payamt = dealerai.dealer_payout.predict(np.array([payout_data]))
             
           #  print('argmax of dealer payout array', np.argmax(payamt), payamt)
             pay_player = dealerai.pay_amounts[np.argmax(payamt)]
             print('result for hand with', player.name, result_txt,'dealer pays ', player.name,pay_player)
             player.money = player.money + pay_player
        return False
                 
class HumanPlayer(player):
      def __init__(self,name="player", isDealer=False, cash=100):
          player.__init__(self,name,isDealer,cash)
          
      def turn(self,dealer_cards,players):
       # self.hand.hit()
        if self.hand.score >= 21 or self.hand.score < 0:
           return False
        choice = input('(h)it, (s)tand, (m)ake ace 11 points or (d)doubledown?\n')   
        if choice=='h' or choice =='':
           # dealer should really be in control of whether the player gets another card or not
           self.hand.hit() 
           self.hand.summary(self.isDealer,False)
           return True
           # could this be a lambda function?
           #score = #self.turn()
           #if self.hand.score == 0 or self.hand.score >= 21 or len(self.hand.cards) == 5:
           #    break  
        elif choice =='m':
             self.hand.make_ace_11()
             return True
        elif choice =='d':
            print('not supported yet')
            return True
        elif choice == 's':
            print('standing pat')
            return False
        else:
           return False   

class NonHumanPlayer(player):
      def __init__(self,name="Robot", isDealer=False, cash=100, threshold=0):
           player.__init__(self,name,isDealer,cash)
           self.card_table = []
           self.threshold = threshold
      def turn(self, dealer_cards,players):
           autoPlayer = autonomousPlayer()
           self.card_table = [list(x.values())[0] for x in self.hand.cards]
           self.hand.ace_promote(self.card_table,autoPlayer.ace_promote_predicters)  
           for i in range(len(self.card_table),5):
               self.card_table.append(0)
           dealer_shows_card = dealer_cards
           self.card_table.append(dealer_shows_card)
           # print('dealer is showing',self.card_table[:5])
           cards = np.array([self.card_table])
           #print('cards used for prediction:', cards)
           count = 0
           for value in self.hand.cards:
                if value ==0:
                   break
                count = count + 1
            #    print(len(self.card_table), 'cards used for prediction', self.card_table)
                prediction = autoPlayer.player_cards[count - 2].predict(cards)
                print('auto player predicts',prediction,'% probability that it should take another card')
                if(prediction.item() > self.threshold):
                    self.hand.hit()
                    self.hand.summary(False,False)
                    return True
                else:
                   # print('autoplayer finishes with', self.hand.cards)
                    return False
