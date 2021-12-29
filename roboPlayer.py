import tensorflow as tf
import pandas as pd
import numpy as np
from tensorflow import keras
from tensorflow.keras import layers
#from keras.models import load_models
import os
from os.path import exists
num_players = 6

raw_training_dataset = pd.read_csv('blkjckhands.csv')
dataset = raw_training_dataset[["card1", "card3","card2","card4","card5","dealcard1","dealcard2", "dealcard3", "dealcard4", "dealcard5", "dlbustbeat"]]
sim_player_dataset = raw_training_dataset[["card1", "card2","card3","card4", "card5","dealcard1","plybustbeat"]]
dealer_pay_dataset = raw_training_dataset[["ply2cardsum","dlbustbeat","sumofcards", "sumofdeal","plwinamt"]]
ace_as_11_dataset = raw_training_dataset[["card1", "card2", "card3", "card4"]]

   # int, str, int, str, int, int
game_results = {'Dlwin':1,'Beat':2,'Bust':3,'PlBust':4,'Push':5, 'Plwin':6, 'DlBust':7}      
winloss_results = {'Loss':0,'Win':1,'Push':2}    
def text_label_to_bool(labels):
    label_bools = []
    for label in labels:
        if label=='Win':
            label_bools.append(1)
        else:
            label_bools.append(0) 
    return label_bools

def results_as_values(results):
     values = []
     for result in results:
         #print(result)
         values.append(game_results[result])
     return values

def winloss_results_as_values(win_loss):
    values = []
    for result in win_loss:
         values.append(winloss_results[result])
    return values
def ace_was_promoted(vals):
     bools = []
     for val in vals:
         bools.append(True if val == 1 else False)
     return bools
         #"blkjck",
         
def game_summary():
   
   if exists('game_summary.csv'):
       game_data = pd.read_csv('game_summary.csv')
       first_col = game_data.columns[0]
       game_data = game_data.drop([first_col], axis=1)
   else:
       data_subset = raw_training_dataset[['dlwinamt', 'plwinamt','sumofcards','sumofdeal']]
       summary = []
       for i, g in data_subset.groupby(np.arange(len(data_subset)) // 6):
           sumofcards = np.array(g['sumofcards'])
           sumofdeal = np.array(g['sumofdeal'])
           player1sum = sumofdeal[0]
           player2sum = sumofdeal[1]
           player3sum = sumofdeal[2]
           player4sum = sumofdeal[3]
           player5sum = sumofdeal[4]
           player6sum = sumofdeal[5]
           dlmoney = sum(g['dlwinamt']) - sum(g['plwinamt'])
           summary.append({'player1sum':player1sum,
                           'player2sum':player2sum,
                           'player3sum':player3sum,
                           'player4sum':player4sum,
                           'player5sum':player5sum,
                           'player6sum':player6sum, 
                           'sumofdeal':sumofdeal[0], 
                           'dlwinamt':dlmoney})
           #print(dlwinnings[:4])
       game_data = pd.DataFrame(summary)
       print('saving game summary data')    
       game_data.to_csv('game_summary.csv')
   return game_data 



# model class
class card_predicter():
     def __init__(self, this_dataset,label,extra,dropout_rate, fifth_layer, output_nodes):
          self.dataset = this_dataset.copy()
          self.label = label
          self.extra = extra
          
       #   self.model
          some_layers = [
                 layers.Dense(128, activation='relu'),
                  layers.Dense(64, activation='relu'),
                  layers.Dense(16,activation='relu'),
                  layers.Dropout(dropout_rate),
                  layers.Dense(output_nodes)]
          if(fifth_layer == True):
              some_layers.insert(0,layers.Dense(512, activation='relu'))
          self.model = keras.models.Sequential(some_layers)
     def card_was_taken(self,vals,categories):
         bools = []
         for val in vals:
            bools.append(1 if val != 0 else 0)
         return bools    
     def to_category(self,inputs,categories):
          output = []
         # print('to_category() got\n',categories,inputs)
          for ip in inputs:
            #  print(ip)
              output.append(categories[ip])
          return output
     def train(self, train_epochs, column, loss_type, categories):
          if self.model_file_exists():
              return
          else:
               print('training', self.label)
              # print(self.dataset)
               #preprocess the label column from floating point numbers to bool in order to use binary cross entropy
               if loss_type == 'binary':
                  loss_function = keras.losses.BinaryCrossentropy(from_logits=True)
                  preprocessing_function = self.card_was_taken
               elif loss_type == 'categorical':
                   loss_function = keras.losses.SparseCategoricalCrossentropy(from_logits=True)
                   preprocessing_function = self.to_category
               elif loss_type == 'numerical':
                   loss_function = keras.losses.MeanSquaredError()
                   preprocessing_function = None
               else:
                  print('specify a loss type for training')
                  return False
               if preprocessing_function != None:
                  t = self.dataset.pop(self.label)
                  self.dataset.insert(column,self.label,preprocessing_function(t,categories)) 
              # print('train() train on',self.dataset)
               self.training_dataset = self.dataset.sample(frac=0.8,random_state=0)
               self.training_labels = self.training_dataset.pop(self.label)
               self.test_features = self.dataset.drop(self.training_dataset.index)
               #print('test features\n',self.test_features)
               self.test_labels = self.test_features.pop(self.label)
               self.training_features = np.array(self.training_dataset.copy())
               self.test_features = np.array(self.test_features)
               #print(self.training_labels)
               self.training_labels = np.array(self.training_labels)
               #self.training_features = np.array(self.training_features)
              # normalizer = tf.keras.layers.Normalization(axis=-1)
               #normalizer.adapt(self.training_features)
               #normalizer.adapt(self.training_labels)
               #normalizer.adapt(self.test_features)
               #normalizer.adapt(self.test_labels)
               print('training shapes',self.training_labels.shape, self.training_features.shape)
               self.model.compile(loss=loss_function,
                                 optimizer=tf.optimizers.Adam(learning_rate=0.001))
               #print("before model.fit()",self.training_labels, self.training_features,'\n---------------------\n')
               self.model.fit(self.training_features,
                              self.training_labels,
                              batch_size = 50,
                              epochs=train_epochs)
               self.model.save(self.label+self.extra+'.h5')               
               self.test_results = self.model.evaluate(self.test_features,
                                                       self.test_labels, 
                                                       batch_size = 100)
     def model_file_exists(self):
          #print("check if ",self.label,self.extra, "exists")
          #print(self.extra)
          if(exists(self.label+self.extra+'.h5')):
              #print('loading model parameters for', self.label)
              
              self.model = keras.models.load_model(self.label+self.extra+'.h5')
              return True
          else:
              return False
     
     def predict(self,input):
         prediction = self.model.predict(input)
         return prediction
###############################################################################################3



batch_size = 100

class BlackjackDealer(card_predicter):
    def __init__(self):
        #  print(dataset)
          dealcard3 = "dealcard3"
          dealcard4 = "dealcard4"
          dealcard5 = "dealcard5"
          self.dataset = dataset.copy()
          self.payout_dataset = dealer_pay_dataset.copy()
          
          self.payout_categories = {0:0, 10:1,20:2,25:3}
          self.game_results = {'Dlwin':0,'Beat':1,'Bust':2,'PlBust':3,'Push':4}
          self.game_result_text = []
          self.pay_amounts = [0,10,20,25]
          # looks like there are 18possible outcomes, not including blackjacks
          #self.dealer_payouts = {60:0,50:1,40:2,30:3,20:4,10:5,0:6,-10:7,-20:8,-30:9,-40:10,-50:11,-60:12,-70:13,-80:14,-90:15,-100:16,-120:17}
          dealcard5_dataset = self.dataset[["card1", "card3","card2","card4","card5","dealcard1","dealcard2", "dealcard3", "dealcard4", "dealcard5"]]
          
          #card predicters and card classifier
          self.dealer_card5 = card_predicter(dealcard5_dataset,dealcard5,"",0,False, 1)
          self.dealer_card4 = card_predicter(self.dataset[["card1", "card3","card2","card4","card5","dealcard1","dealcard2", "dealcard3", "dealcard4"]],dealcard4, "",0,False,1)
          self.dealer_card3 = card_predicter(self.dataset[["card1", "card3","card2","card4","card5","dealcard1","dealcard2", "dealcard3"]],dealcard3,"",0, False,1)
          #results = self.dataset.pop('dlbustbeat')
          #self.dataset.insert(1,'dlbustbeat',results_as_values(results))
          self.dealer_result_classifier = card_predicter(self.dataset,"dlbustbeat","",0, False,5)
         # self.dealer_result_classifier_4 = card_predicter(self.dataset["card1", "card3","card2","card4","card5","dealcard1","dealcard2"],"dlbustbeat","",0, False)
         # self.dealer_result_classifier_3 = card_predicter(self.dataset["card1", "card3","card2","card4","card5","dealcard1","dealcard2"],"dlbustbeat","",0, False)
         # self.dealer_result_classifiers = [self.dealer_result_classifier_3, self.dealer_result_classifier_4, self.dealer_result_classifier_5]
          ds = game_summary()
          self.dealer_game_result_analyzer = card_predicter(ds,"dlwinamt","",0,True,1)
          self.ace_promote_predicter_1 = card_predicter(ace_as_11_dataset[["card1", "card2"]],"card1","dealer_ace",0, True,1)
          self.ace_promote_predicter_2 = card_predicter(ace_as_11_dataset[["card1", "card2"]],"card2","dealer_ace",0, True,1)
          self.ace_promote_predicters = [self.ace_promote_predicter_1,self.ace_promote_predicter_2]
          # self.dealer_ace_promote_predicter = (ace_as_11_dataset,,0,False)
          self.dealer_cards = [self.dealer_card3, self.dealer_card4,self.dealer_card5]
          self.dealer_card3.train(5,1,'binary',None)
          self.dealer_card4.train(5,3,'binary',None)
          self.dealer_card5.train(5,4,'binary',None)
          
          #these last two models should be categorical- rather than binary-crossentropy. So they also need a different preprocessing function to convert labels into categories 
          self.dealer_result_classifier.train(4,9,'categorical',self.game_results)
          results = self.payout_dataset.pop('dlbustbeat')
          self.payout_dataset.insert(1,'dlbustbeat',self.to_category(results,self.game_results))
          self.dealer_payout = card_predicter(self.payout_dataset,"plwinamt","",0.04, False,4)
          self.dealer_payout.train(5,4,'categorical',self.payout_categories)
          
          self.dealer_game_result_analyzer.train(10,6,'numerical',None)
          self.ace_promote_predicter_1.train(3, 0, 'binary',None)
          self.ace_promote_predicter_2.train(3, 1, 'binary',None)
   #  def predict_card(self,card):
                              
class autonomousPlayer(card_predicter):
    def __init__(self):
          #print(sim_player_dataset)
          self.dataset = sim_player_dataset.copy()
          player_results = self.dataset.pop('plybustbeat')
          self.dataset.insert(6,'plybustbeat',results_as_values(player_results))
         # print(self.dataset)

          self.player_card5 = card_predicter(self.dataset,"card5","",0, False,1)
          self.player_card4 = card_predicter(self.dataset,"card4","",0, False,1)
          self.player_card3 = card_predicter(self.dataset,"card3","",0, False,1)
          self.player_cards = [self.player_card3,self.player_card4,self.player_card5]
          self.ace_promote_predicter_4 = card_predicter(ace_as_11_dataset,"card4","ace",0, True,1)
          self.ace_promote_predicter_3 = card_predicter(ace_as_11_dataset[["card1", "card2", "card3"]],"card3","ace",0, True,1)
          self.ace_promote_predicter_2 = card_predicter(ace_as_11_dataset[["card1", "card2"]],"card2","ace",0, True,1)
          self.ace_promote_predicter_1 = card_predicter(ace_as_11_dataset[["card1", "card2"]],"card1","ace",0, True,1)
          self.ace_promote_predicters = [self.ace_promote_predicter_1, self.ace_promote_predicter_2, self.ace_promote_predicter_3,self.ace_promote_predicter_4                                         ]
          
          
         # #if dealer_card3.model_file_exists() ==False:
          self.player_card3.train(5, 1, 'binary',None)
          #if dealer_card4.model_file_exists() ==False:
          self.player_card4.train(3, 3, 'binary',None)
          #if dealer_card5.model_file_exists() ==False:
          self.player_card5.train(3, 4, 'binary',None)         
          
          self.ace_promote_predicter_1.train(3, 0, 'binary',None)
          self.ace_promote_predicter_2.train(3, 1, 'binary',None)
          self.ace_promote_predicter_3.train(3, 2, 'binary',None)
          self.ace_promote_predicter_4.train(3, 3, 'binary',None)                     
#if(len.sys.argv) ==2:
#     if(sys.argv[1] == 'retrain'):
     
#         os.remove('dealcard3.h5)
#         os.remove('dealcard4.h5)
#         os.remove('dealcard5.h5)    
#print(dataset.head())      
sammy = BlackjackDealer()

#simulated_game_data = [20,17,17,15,19,15,18]
#print('predict dealer win amount',sammy.dealer_game_result_analyzer.predict(np.array([simulated_game_data])))

#"ply2cardsum","dlbustbeat","sumofcards", "sumofdeal","plwinamt"
#payout_test_data = [20,1,20,18]# [11,,21,21]
                   
#r = sammy.dealer_payout.predict(np.array([payout_test_data]))
#print('payout test', r) 
#def get_dealer_winnings(game):
#     return raw_training_dataset['dlwinamt'][game:game+6]
#dealer_winnings = [win for winraw_training_dataset['dlwinamt'][0:6]]

Johnny = autonomousPlayer()
#Sally = autonomousPlayer()          
#y('predict 2 card Blackjack', Johnny.ace_promote_predicter_1.predict(np.array([[10],[9],[8],[7],[6],[5],[4],[3],[2],[1]]) ))
#print('predict 2 card Blackjack', Johnny.ace_promote_predicter_2.predict(np.array([[10],[9],[8],[7],[6],[5],[4],[3],[2],[1]]) ))
#print('predict based on \n', sammy.dealer_card3.test_features[0:1])
#print('predict payout', sammy.dealer_payout.predict(sammy.dealer_payout.test_features[0:4]))

#sample_game = np.array([[10,7,0,0,0,5,8,0,0,]])
#