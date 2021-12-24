# Import required modules
from random import shuffle



# Define a class to create
# all type of cards
class Cards:
	global suites, values
	suites = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
	values = [{'A':1}, {'2':2}, {'3':3}, {'4':4}, {'5':5},{'6':6}, {'7':7},
		  {'8':8}, {'9':9}, {'10':10}, {'J':10}, {'Q':10}, {'K':10}]
	
	def __init__(self):
		pass
	def value(self,which):
		return points[which]


# Define a class to categorize each card
class Deck(Cards):
    def __init__(self):
        Cards.__init__(self)
        self.mycardset = []
        for n in suites:
            for c in values:
                for v in c.values():
                   #if v == 1:
                   #    v = 'ace'
                   cardName = str(v)+" "+"of"+" "+n
                   #self.mycardset.append({(c)+" "+"of"+" "+n:})
                   self.mycardset.append({cardName:v})
                   self.mycardset

    # Method to remove a card from the deck
    def popCard(self):
        if len(self.mycardset) == 0:
           return "NO CARDS CAN BE POPPED FURTHER"
        else:
            cardpopped = self.mycardset.pop()
            print("Card removed is", cardpopped)


# Define a class gto shuffle the deck of cards
class ShuffleCards(Deck):

	# Constructor
	def __init__(self):
		Deck.__init__(self)

	# Method to shuffle cards
	def shuffle(self):
		if len(self.mycardset) < 52:
			print("cannot shuffle the cards")
		else:
			shuffle(self.mycardset)
			return self.mycardset

	# Method to remove a card from the deck
	def popCard(self):
		if len(self.mycardset) == 0:
			return "NO CARDS CAN BE POPPED FURTHER"
		else:
			cardpopped = self.mycardset.pop()
			return (cardpopped)

