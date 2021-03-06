"""
Ryan Kinsella
10194574
15rklk
Forty Thieves Autostart Algorithm
"""
import random
import copy
import time

"""____________________Global Variables___________________"""
# To be used with the Card object
suits = ['Hearts','Diamonds','Spades','Clubs']
cardFaces = ['A','2','3','4','5','6','7','8','9','10','J','Q','K']
# Constants, can be changed to whatever as long as the deck holds as many cards as needed
k = 2
n = 10
m = 4
p = 8
cards = []
stacks = [[None for x in range(m)] for y in range(n)] #Stacks
piles = [[None for a in range(len(cardFaces))] for b in range(p)] #Piles
allNodes = []
"""____________________Global Variables___________________"""


"""_____________________________________Card Object__________________________________________"""
# suit: string, used in comparisons
# face: string, used to determine hierarchy
class Card(object):
    # initialization
    def __init__(self, suit, face): #string, string
        self.face = face
        self.suit = suit
    # Used for testing purposes
    def display(self):
        print(self.face, "of", self.suit)
    # String return
    def getInfo(self):
        return self.face + " of " + self.suit
"""_____________________________________Card Object__________________________________________"""

"""_____________________________________Node Object__________________________________________"""
class Node(object):
    # initialization
    def __init__(self, card, depth, previousStack, previousPiles): # card Object, int, 2D array, 2D array
        self.card = card
        # Python requires copies of lists to be created for faces used in pervious nodes,
        # otherwise variables don't copy over

        self.stacks = previousStack
        self.piles=previousPiles
        self.depth = depth
        self.nextDepth = depth+1
        self.nextCards = []
        self.topCards = []
        self.children = []

        aCard = Card('nothing', 'nothing')
        for i in range(0, len(self.stacks)): # O(n)
            if len(self.stacks[i]) > 0:
                # if there are still cards in the stack, add them to the top of each stack at index 0
                self.topCards.append(self.stacks[i][0])
            else:
                self.topCards.append(aCard) # add a blank card below to avoid index errors
        for i in range(0, p): # O(p) , for each pile
            if self.piles[i][0] != None: # if pile is not empty
                active = self.piles[i][0] # active card for each pile
                faceValue = getIndex(active.face)
                if faceValue > 12: # if a king is on top of the pile
                    theFace = 'X'  # placeholder for king + 1
                else:
                    theFace = cardFaces[faceValue + 1]
                # Indexing requires that a card will always need to be added
                newCard = Card(active.suit, theFace)
                self.nextCards.append(newCard)
            else:
                # create this 'necessary' card, and then add it to the list of cards that are needed
                newCard = Card('AnySuit', 'A') # Create a card with any suit and value Ace
                self.nextCards.append(newCard)

        # Used for testing purposes within initialization
        # print ("Starting Cards", self.depth)
        # for i in range (0, len(self.topCards)):
        #     self.stacks[i][0].display()

    # Used for testing purposes only
    def moveCard(self, theCard, startIndex, endIndex):
        print ("Before Piles:")
        self.displayStartAndEndPiles()
        self.piles[endIndex].insert(0,theCard)
        self.stacks[startIndex].pop(0)
        print ("After Piles:")
        self.displayStartAndEndPiles()


    def makeChildren(self):
        # Used for testing purposes
        # print ("Creating children with node depth: ", self.depth)
        # for i in range (0,len(self.topCards)):
        #     self.topCards[i].display()
        # print ("break")
        # for i in range (0,len(self.nextCards)):
        #     self.nextCards[i].display()
        for s in range(0,len(self.stacks)): # for each stack
            cFound = False
            pilesCount = 0
            while pilesCount < len(self.piles) and cFound == False: # for each pile if no cards are found
                aCard=self.topCards[s]
                bCard=self.nextCards[pilesCount]
                cFound = areCardsEqual(aCard,bCard)
                if cFound:
                    theStacks = copy.deepcopy(self.stacks)
                    thePiles = copy.deepcopy(self.piles)
                    thePiles[pilesCount].insert(0, self.stacks[s][0])
                    theStacks[s].pop(0)
                    n1 = Node(self.stacks[s][0], self.nextDepth, theStacks, thePiles)
                    self.children.append(n1)
                pilesCount +=1

    def returnChildren(self):
        return self.children

    # Used for testing purposes
    def displayStartAndEndPiles(self):
        count = 0
        print("___________Starting piles:___________")
        while count < n:
            if len(self.stacks[count]) > 0:
                active = self.stacks[count][0]
                print("Starting Pile", count + 1, ": ", active.getInfo())
            else:
                print("Starting Pile", count + 1, ": empty.")
            count += 1
        count = 0
        print("____________Ending piles:____________")
        while count < p:
            if self.piles[count][0] != None:
                print("Ending Pile", count + 1, ": ", self.piles[count][0].getInfo())
            else:
                print("Ending Pile", count + 1, ": empty.")
            count += 1
"""_____________________________________Node Object__________________________________________"""


# Returns true if the two cards are equal, false if not
def areCardsEqual(card1, card2):
    if card1.suit == card2.suit and card1.face == card2.face:
        return True
        # print ("______Match Found_____")
    elif card1.face == 'A' and card2.face == 'A':
        return True
        # print ("______Match Found_____")
    else:
        return False

# get index of the next face that needs to be found to find out what the next card necessary will be
def getIndex(toFind):
    global cardFaces
    found = 0
    count = 0
    # find index of required face, scroll through list until found
    while found == 0:
        if toFind == cardFaces[count]:
            found = 1
        else:
            count += 1
    return count


def createDeck():
    global cards
    global cardFaces
    global suits
    for i in range(0,4): # for each suit
        for j in range (0,13): # for each face value
                for z in range (0,k): # for each deck
                    ca = Card (suits[i],cardFaces[j])
                    cards.append(ca)
    random.shuffle(cards)

def dealDeckIntoStacks():
    global cards
    global stacks
    deckIndex = 0
    for i in range(0, n): # for each stack
        for j in range(0, m): # for the number of cards required per stack
            stacks[i][j] = cards[deckIndex] # for each card within deck, deal
            deckIndex += 1
    # Used as an example from Figure 1
    # c1 = Card ('Hearts', 'A')
    # c2 = Card ('Diamonds', 'A')
    # c3 = Card('Diamonds', '2')
    # c4 = Card('Diamonds', '2')
    # c5 = Card('Diamonds', 'K')
    # c6 = Card('Hearts', '2')
    # stacks[0].insert(0,c1)
    # stacks[0].insert(1, c3)
    # stacks[0].insert(2, c5)
    # stacks[1].insert(0,c2)
    # stacks[1].insert(1, c4)
    # stacks[1].insert(2, c6)

# return True if game is over
def canGameContinue(depth, theList):
    found = False
    count = 0
    while found == False and count < len(theList):
        if theList[count].depth == depth:
            found = True
        else:
            count += 1
    return found

#_________________________________________________Main__________________________________________________________________

"""
#_______________________Use this main to run multiple times for a target max_________________________
iterations=0
maximum = 0
listOfMax0=[]
listOfMax1=[]
listOfMax2=[]
listOfMax3=[]
listOfMax4=[]
listOfMax5=[]
listOfMax6=[]
listOfMax7=[]
listOfMax8=[]
listOfMax9=[]
listOfMax10=[]
listOfMax11=[]
listOfMax12=[]
listOfMax13=[]
listOfMax14=[]

startTime = time.time()
while maximum < 10:
    activeNodes = []
    childNodes = []
    createDeck()
    dealDeckIntoStacks()
    root = Node (None, 0, stacks, piles)
    allNodes.append(root)
    activeNodes.append(root)
    continuePlaying = True
    targetDepth = 0

    while continuePlaying and targetDepth < 15:
        continuePlaying = canGameContinue(targetDepth, allNodes)
        targetDepth +=1
        for i in range (0,len(activeNodes)):
            curr = activeNodes[i]
            curr.makeChildren()
            childNodes = curr.returnChildren()
        activeNodes = childNodes
        childNodes = []
        allNodes.extend(activeNodes)


    # Used for testing, ending list
    # for i in range (0, len(allNodes)):
    #     print()
    #     curr = allNodes[i]
    #     print ("Current node depth of:",curr.depth)
    #     curr.displayStartAndEndPiles()
    # print ("DONE NOW")
    #

    maximum = 0
    loc =0
    for i in range (0,len(allNodes)):
        if allNodes[i].depth > maximum:
            maximum = allNodes[i].depth
            loc = i

    if maximum==0:
        listOfMax0.append(maximum)
    elif maximum==1:
        listOfMax1.append(maximum)
    elif maximum==2:
        listOfMax2.append(maximum)
    elif maximum==3:
        listOfMax3.append(maximum)
    elif maximum==4:
        listOfMax4.append(maximum)
    elif maximum==5:
        listOfMax5.append(maximum)
    elif maximum==6:
        listOfMax6.append(maximum)
    elif maximum==7:
        listOfMax7.append(maximum)
    elif maximum==8:
        listOfMax8.append(maximum)
    elif maximum==9:
        listOfMax9.append(maximum)
    elif maximum==10:
        listOfMax10.append(maximum)
    elif maximum==11:
        listOfMax11.append(maximum)
    elif maximum==12:
        listOfMax12.append(maximum)
    elif maximum==13:
        listOfMax13.append(maximum)
    elif maximum == 14:
        listOfMax14.append(maximum)

    iterations+=1
    allNodes=[]

print("Max of 0:",len(listOfMax0))
print("Max of 1:",len(listOfMax1))
print("Max of 2:",len(listOfMax2))
print("Max of 3:",len(listOfMax3))
print("Max of 4:",len(listOfMax4))
print("Max of 5:",len(listOfMax5))
print("Max of 6:",len(listOfMax6))
print("Max of 7:",len(listOfMax7))
print("Max of 8:",len(listOfMax8))
print("Max of 9:",len(listOfMax9))
print("Max of 10:",len(listOfMax10))
print("Max of 11:",len(listOfMax11))
print("Max of 12:",len(listOfMax12))
print("Max of 13:",len(listOfMax13))
print("Max of 14:",len(listOfMax14))
print ("Max number of cards placed on piles:", maximum, "after" ,iterations,"iterations")
print("Runtime: %s seconds" % (time.time() - startTime))
#_______________________Use this main to run multiple times for a target max_________________________
"""

"""


#__________________Use this main to show a single result step by step____________________



activeNodes = []
childNodes = []
createDeck()
dealDeckIntoStacks()
root = Node (None, 0, stacks, piles)
allNodes.append(root)
activeNodes.append(root)
continuePlaying = True
targetDepth = 0
while continuePlaying and targetDepth < 15: # O(2^15)
    continuePlaying = canGameContinue(targetDepth, allNodes)
    targetDepth +=1
    for i in range (0,len(activeNodes)): # O(2^targetDepth)
        curr = activeNodes[i]
        curr.makeChildren()
        childNodes = curr.returnChildren()
    activeNodes = childNodes
    childNodes = []
    allNodes.extend(activeNodes)

##ENDING LIST
for i in range (0, len(allNodes)):
    print()
    curr = allNodes[i]
    print ("Node depth of:",curr.depth)
    curr.displayStartAndEndPiles()

maximum = 0
loc =0
for i in range (0,len(allNodes)):
    if allNodes[i].depth > maximum:
        maximum = allNodes[i].depth
        loc = i

print()
print ("____________Finished, displaying final node results:____________")
print()
allNodes[loc].displayStartAndEndPiles()
print()
print ("the number of cards that were dealt is:" , maximum)


#__________________Use this main to show a single result step by step____________________
"""
