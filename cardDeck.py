from random import shuffle

class card:
   def __init__(self,name):
      self.taken = false
      self.name = name

class suit:
   def __init__(self,name):
      self.name=name

   cardValues =  {"A":1,
                  "2":2,
                  "3":3,
                  "4":4,
                  "5":5,
                  "6":6,
                  "7":7,
                  "8":8,
                  "9":9,
                  "J":10,
                  "Q":10,
                  "K":10}
    card cardsInSuit = [card("A"),
                        card("2"),
                        card("3"),
                        card("4"),
                        card("5"),
                        card("6"),
                        card("7"),
                        card("8"),
                        card("9"),
                        card("J"),
                        card("Q"),
                        card("K")]
class deck:
   def __init__(self):
      cardsInDeck = [suit("hearts",suit("spades"),suit("diamonds",suit("clubs")]

   def dealCard(show):
     print('placeholder')

   def shuffle():

card("2"),
