import tensorflow as tf
import pandas as pd
import numpy as np
from tensorflow import keras
from tensorflow.keras import layers
#from keras.models import load_models
import os
from os.path import exists
num_players = 6
card3 = "dealcard3"
card4 = "dealcard4"
card5 = "dealcard5"
raw_training_dataset = pd.read_csv('blkjckhands.csv')
dataset = raw_training_dataset[["card1", "card3","card2","card4","card5","dealcard1","dealcard2", "dealcard3", "dealcard4", "dealcard5", "dlbustbeat"]]
sim_player_dataset = raw_training_dataset[["card1", "card2","card3","card4", "card5","dealcard1","plybustbeat"]]
   # int, str, int, str, int, int
game_results = {'Dlwin':1,'Beat':2,'Bust':3,'PlBust':4,'Push':5, 'Plwin':6, 'DlBust':7}          
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


dealer_pay_dataset = raw_training_dataset[["ply2cardsum","dlbustbeat","sumofcards","blkjck", "sumofdeal","plwinamt"]]
results = dataset.pop('dlbustbeat')
dataset.insert(10,'result',results_as_values(results))
player_results = sim_player_dataset.pop('plybustbeat')
sim_player_dataset.insert(6,'player_result',results_as_values(player_results))
#gameResultsDataset = raw_training_dataset[["sumofcards","sumofdeal","dlbustbeat"]]
       

dealer_pay_dataset.pop('dlbustbeat')
dealer_pay_dataset.insert(1,'dlbustbeat',results_as_values(results))
player_blackjack = dealer_pay_dataset.pop('blkjck') 
dealer_pay_dataset.insert(3,'blkjck',text_label_to_bool(player_blackjack)) 
#print(dealer_pay_dataset)
# model class
class card_predicter():
     def __init__(self, dataset,label,dropout_rate):
          self.dataset = dataset
          self.label = label
          #print(self.label,self.dataset)
          #results = dataset['dlbustbeat']
          #print(results)
         # dataset.pop('dlbustbeat')
         # self.dataset.insert(11,'result',results_as_values(results))
         # print(self.dataset)
          
       #   self.model
          self.model = keras.models.Sequential([
                  #layers.Dense(2048, activation='relu'),
                  #layers.Conv1D(32,2,activation='relu', input_shape = (11,1)),
                  #layers.MaxPooling1D(2,1),
                  #layers.Conv1D(16,2,activation='relu'),
                  #layers.MaxPooling1D(2,1),
                  
                #  layers.Dense(768, activation='relu'),
                  layers.Dense(128, activation='relu'),
                  layers.Dense(64, activation='relu'),
                  layers.Dense(16,activation='relu'),
                  layers.Dropout(dropout_rate),
                  layers.Dense(1)])
         
     def train(self, train_epochs):
          if self.model_file_exists():
              return
          else:
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
               normalizer = tf.keras.layers.Normalization(axis=-1)
               normalizer.adapt(self.training_features)
               normalizer.adapt(self.training_labels)
               normalizer.adapt(self.test_features)
               normalizer.adapt(self.test_labels)
              
               self.model.compile(loss=keras.losses.MeanSquaredError(),
                                 optimizer=tf.optimizers.Adam(learning_rate=0.001))
               self.model.fit(self.training_features,
                              self.training_labels,
                              batch_size = 50,
                              epochs=train_epochs)
               self.model.save(self.label+'.h5')               
               self.test_results = self.model.evaluate(self.test_features,
                                                       self.test_labels, 
                                                       batch_size = 100)
     def model_file_exists(self):
          if(exists(self.label+'.h5')):
              #print('loading model parameters for', self.label)
              self.model = keras.models.load_model(self.label+'.h5')
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
          self.dealer_card5 = card_predicter(dataset,card5,0)
          self.dealer_card4 = card_predicter(dataset,card4,0)
          self.dealer_card3 = card_predicter(dataset,card3,0)
          self.dealer_result_classifier = card_predicter(dataset,"result",0)
          self.dealer_payout = card_predicter(dealer_pay_dataset,"plwinamt",0.04)
          self.dealer_cards = [self.dealer_card3, self.dealer_card4,self.dealer_card5]
          #if dealer_card3.model_file_exists() ==False:
          self.dealer_card3.train(10)
          #if dealer_card4.model_file_exists() ==False:
          self.dealer_card4.train(5)
          #if dealer_card5.model_file_exists() ==False:
          self.dealer_card5.train(5)
          self.dealer_result_classifier.train(5)
          self.dealer_payout.train(10)
   #  def predict_card(self,card):
                              
class autonomousPlayer(card_predicter):
    def __init__(self):
          self.player_card5 = card_predicter(sim_player_dataset,"card5",0)
          self.player_card4 = card_predicter(sim_player_dataset,"card4",0)
          self.player_card3 = card_predicter(sim_player_dataset,"card3",0)
          self.player_cards = [self.player_card3, self.player_card4,self.player_card5]
          #if dealer_card3.model_file_exists() ==False:
          self.player_card3.train(10)
          #if dealer_card4.model_file_exists() ==False:
          self.player_card4.train(5)
          #if dealer_card5.model_file_exists() ==False:
          self.player_card5.train(5)                              
#if(len.sys.argv) ==2:
#     if(sys.argv[1] == 'retrain'):
     
#         os.remove('dealcard3.h5)
#         os.remove('dealcard4.h5)
#         os.remove('dealcard5.h5)          
#sammy = BlackjackDealer()
#Johnny = autonomousPlayer()
          
#print('predict based on \n', sammy.dealer_card3.test_features[0:1])
#print('predict payout', sammy.dealer_payout.predict(sammy.dealer_payout.test_features[0:4]))

#sample_game = np.array([[10,7,0,0,0,5,8,0,0,]])
#print('sample game:', sample_game)
#prediction = sammy.dealer_card3.predict(sample_game)
#print(prediction)
#test_features[game*6:game*6+1]) > 0.5
#for game in range(10):
#    print('predict based on \n', sammy.dealer_card3.test_features[game*6:game*6+1])
#    prediction = sammy.dealer_card3.predict(sammy.dealer_card3.test_features[game*6:game*6+1])
#    print(prediction)
#    if(prediction < 0.5):
#         continue
#    prediction = sammy.dealer_card4.predict(sammy.dealer_card4.test_features[game*6:game*6+1])
#    print(prediction)
#    if(prediction < 0.5):
#         continue
#    prediction = sammy.dealer_card5.predict(sammy.dealer_card5.test_features[game*6:game*6+1])
    #prediction = model.predict(sample_game) 
#    print(prediction)
