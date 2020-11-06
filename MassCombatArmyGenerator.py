import pandas as pd
import random as rd
import numpy as np

# this class presently does not do anything
class element:

    def __init__(self, name, TS, SupTS, classes, supclasses, traits, cost):
        self.name = name
        self.TS = TS
        self.SupTS = SupTS
        self.classes = classes
        self.supclasses = supclasses
        self.traits = traits
        self.cost = cost

# create a .csv file with the requisite columns, and set it to the used .csv
def NewArmy():
    try: 
        ArmyName = input("What would you like to call your army? ")
        DF1 = pd.DataFrame(columns = ['name', 'TS', 'Sup', 'classes', 'supclasses', 'cost'])
        DF1.to_csv(ArmyName + '.csv', index=False)
        global myCSV
        myCSV = str(ArmyName + '.csv')
    except:
        print("Unable to create new army file.")

# create an element to populate the selected .csv file
def NewElement():
    try:
        df = pd.read_csv(myCSV, delimiter=',')
    except:
        print("No army file detected. Cannot build new element.")
        return

    Succ = False
    while Succ == False: 
        try: 
            EleName = str(input("What is this element called? "))
            EleTS = int(input("What is this Element's TS? "))
            EleSup = str(input("Is this a support element? (Y/N) "))
            if "y" in EleSup:
                EleSup = "Y"
            else:
                EleSup = "N"
            print("Available classes: air  arm  art  c3i  cv  eng  f  rec")
            EleClasses = str(input("What are this element's classes? "))
            if "air" or "arm" or "art" or "c3i" or "cv" or "eng" or "f" or "rec" not in EleClasses.lower():
                EleClasses = "Na"
            EleSupClasses = str(input("What are this element's support classes? "))
            if "air" or "arm" or "art" or "c3i" or "cv" or "eng" or "f" or "rec" not in EleSupClasses.lower():
                EleSupClasses = "Na"
            EleCost = int(input("What is this element's cost? "))
        except ValueError:
            print(
            "Sorry, your most recent value was invalid.\nNote that TS and cost must be intergers"
                )
        else:
            Succ = True
    
    newrow = pd.DataFrame({
        'name':[EleName], 'TS':[EleTS], 'Sup':[EleSup], 'classes':[EleClasses.lower()],
        'supclasses':[EleSupClasses.lower()], 'cost':[EleCost]
    })

    df = df.append(newrow, ignore_index=True)

    df.to_csv(myCSV, index=False, mode='w')

# load a .csv into a dataframe, and randomly take rows from that dataframe and put them in another 
# dataframe until the second dataframe's "TS" column is equal to what the user inputs
def buildarmy():
    # set variables for algorithm to use
    succ_BA = False
    try: 
        ArmyList = pd.read_csv(myCSV, delimiter=',')
    except:
        print("No army file detected. Failed to build army.")
        return
    while succ_BA == False: 
        try: 
            TSgoal = int(input("What is your target TS? "))
        except ValueError:
            print("Error: target TS must be an interger.")
        else: 
            succ_BA = True
    TSactual = 0


    Army = pd.DataFrame(columns = ['name', 'TS', 'Sup', 'classes', 'supclasses', 'cost'])
    ListSize = len(ArmyList)-1
    CurrentClass = ['air', 'arm', 'art', 'c3i', 'cv', 'eng', 'f','rec']
    MaxTS = int(ArmyList['TS'].max())
    
    # fix input TS being too high to calculate quickly/effectively randomize
    if TSgoal > 100*MaxTS:
        TSquotient = int(TSgoal/MaxTS)
        goalDivisor = 10**(int(len(str(TSquotient)))-2)
        TSgoal = TSgoal/goalDivisor
    else:
        goalDivisor = 1
    if MaxTS > 0.5*TSgoal:
        listAccuracy = 0.5
    else:
        listAccuracy = 0.95
        
    # actual randomization algorithm
    while TSactual < TSgoal:
        # fill to 95% of TS goal, undo last addition if it goes over the TS goal
        while TSactual < (listAccuracy*TSgoal):
            RandomUnit = rd.randint(0, ListSize)
            TSgap = MaxTS/int(ArmyList['TS'].iloc[[RandomUnit]])
            Equalizer = int(TSgap)

            # 10 Infantry = 1 Dragon because of this
            for i in range(0, Equalizer):
                Army = Army.append(ArmyList.iloc[[RandomUnit]], ignore_index=True)
                TSactual = TSactual + int(ArmyList['TS'].iloc[[RandomUnit]])

            if TSactual > (TSgoal):
                Army = Army[:-1]
                TSactual -= int(ArmyList['TS'].iloc[[RandomUnit]])
 
        # set variables for algorithm to use to determine how best to fill the final 5%
        Remainder = TSgoal - TSactual
        ClosestUnit = np.argmin(abs(ArmyList['TS']-Remainder))
        NextUp = np.argmin(abs(ArmyList['TS']-(Remainder/2)))
        Smallest = np.argmin(ArmyList['TS'])
        
        # find the closest row to fill the final 5% using the previous variables, repeat until finished
        if (ArmyList['TS'].iloc[ClosestUnit] + TSactual) <= TSgoal:
            Army = Army.append(ArmyList.iloc[ClosestUnit], ignore_index=True)
            TSactual += int(ArmyList['TS'].iloc[[ClosestUnit]])
        elif (ArmyList['TS'].iloc[NextUp] + TSactual) <= TSgoal:
            Army = Army.append(ArmyList.iloc[NextUp], ignore_index=True)
            TSactual += int(ArmyList['TS'].iloc[NextUp])
        elif (ArmyList['TS'].iloc[Smallest] + TSactual) <= TSgoal:
            Army = Army.append(ArmyList.iloc[Smallest], ignore_index=True)
            TSactual += int(ArmyList['TS'].iloc[[Smallest]])
        else:
            break

    while TSactual > TSgoal:
        Remainder = TSgoal - TSactual
        ClosestUnit = np.argmin(abs(ArmyList['TS']+Remainder))
        NextUp = np.argmin(abs(ArmyList['TS']+(Remainder/2)))
        Smallest = np.argmin(ArmyList['TS'])
        if (ArmyList['TS'].iloc[ClosestUnit] + TSactual) <= TSgoal:
            Army = Army.remove(ArmyList.iloc[ClosestUnit], ignore_index=True)
            TSactual -= int(ArmyList['TS'].iloc[[ClosestUnit]])
        elif (ArmyList['TS'].iloc[NextUp] + TSactual) <= TSgoal:
            Army = Army.remove(ArmyList.iloc[NextUp], ignore_index=True)
            TSactual -= int(ArmyList['TS'].iloc[NextUp])
        elif (ArmyList['TS'].iloc[Smallest] + TSactual) <= TSgoal:
            Army = Army.remove(ArmyList.iloc[Smallest], ignore_index=True)                
            TSactual -= int(ArmyList['TS'].iloc[[Smallest]])
        else:
            Army = Army[:-1]
            TSactual -= int(ArmyList['TS'].tail(1))            
                
    # Count 'support' TS.
    ClassA = pd.DataFrame(columns = ['name', 'TS', 'Sup', 'classes', 'supclasses', 'cost'])
    for i in range(len(Army)):
        if 'Y' in Army['Sup'].iloc[i]:
            ClassA = ClassA.append(Army.iloc[i], ignore_index=True)

    # Display army, total TS, and total cost
    #print(Army)
    print("")
    print(Army['name'].value_counts())
    print("")
    print('Total TS: ' + str(Army['TS'].sum()*goalDivisor))
    print('Effective TS: ' + str(int((Army['TS'].sum()-(ClassA['TS'].sum()*0.9))*goalDivisor)))
    print('Total cost: $' + str(Army['cost'].sum()*goalDivisor))
    print('Support TS: ' + str(ClassA['TS'].sum()*goalDivisor))

    # Count and display TS for special class superiority
    print("\nSpecial class TS totals: ")
    ClassB = pd.DataFrame(columns = ['name', 'TS', 'Sup', 'classes', 'supclasses', 'cost'])
    ClassC = pd.DataFrame(columns = ['name', 'TS', 'Sup', 'classes', 'supclasses', 'cost'])

    for x in range(len(CurrentClass)):
        for i in range(len(Army)):
            if CurrentClass[x] in Army['classes'].iloc[i]:
                ClassB = ClassB.append(Army.iloc[i], ignore_index=True)
            elif CurrentClass[x] in Army['supclasses'].iloc[i]:
                ClassC = ClassC.append(Army.iloc[i], ignore_index=True)
        if ClassC['TS'].sum() > 0: 
            print(str(CurrentClass[x]) + ": " + str(ClassB['TS'].sum()*goalDivisor) + " + " + str(ClassC['TS'].sum()*goalDivisor) + ' Neutralize')
        else:
            print(str(CurrentClass[x]) + ": " + str(ClassB['TS'].sum()*goalDivisor))
        ClassB = ClassB.iloc[0:0]
        ClassC = ClassC.iloc[0:0]
    print("")

# Select the .csv file to use
def ChooseArmy(): 
    succ_CA = False
    while succ_CA == False: 
        try: 
            ArmySelect = input("Input the title of the file you wish to load (do not include the file extension): ")
            global myCSV
            myCSV = str(ArmySelect + '.csv')
            ArmyList = pd.read_csv(myCSV, delimiter=',')
            print(ArmyList)
        except:
            print("Sorry, no such file was found in the folder this program is in. Try again.")
            myCSV = "NaN"
            succ_CA = True
        else:
            succ_CA = True

# Display the current .csv file in use on the menu. 
def CurrentFile():
    try:
        print("Current file: " + myCSV)
    except NameError:
        print("Current file: NaN")

def describeMe():
    try: 
        ArmyList = pd.read_csv(myCSV, delimiter=',')
    except:
        print("No army file detected. Failed to build army.")
        return
    else:
        print("Average TS: " + ArmyList['TS'].mean())
        print("")

def Tutorial():
    print(
    "\nEach function of this program is simple, but may not work the way you expect. Here are some tips:\n"
    "\n"
    "New army - creates a new formatted .csv file. The columns are: 'name,TS,Sup,classes,supclasses,cost'.\n"
    "name is the element's name, TS is its troops score as an interger, 'Sup' is whether or not its TS is parenthetical.\n"
    "classes are its non-parenthetical classes, supclasses are parenthetical classes (IE neutralize), and cost is the raise value as an interger.\n"
    "The classes are: air, arm, art, c3i, cv, eng, f, rec. Remember that these are CaSe SeNsItIvE.\n"
    "\n"
    "New element - Just follow the instructions and remember that everything is case sensitive.\n"
    "\n"
    "Choose army .csv file - The file needs to be in the same folder as this program. It can be any .csv file formatted as above.\n"
    "\n"
    "Build randomized army - This is the actual point of the program. Remember to load in a .csv file before\n"
    "you run this. You will be asked for a target TS, and from there the program will generate your army for you.\n"
    "It randomly selects elements from the list, and tallies the army's basic stats.\n"
    "Total TS is simply that, a TS total. Effective TS factors in support units and is what is used for\n"
    "relative TS calculations. Cost is dollar cost to raise the entire force.\n"
    "Note that the algorithm is biased to undershoot rather than overshoot input TS.\n"
    "Because of this, relatively low target TS scores (ie. smaller than two of your highest TS units) may produce wonky armies.\n"
    "\n"
    "Re-jigging the probabilities - the program selects rows from the .csv at equal probability. Each row is\n"
    "Represenative of one element. Think of it as drawing from a deck of cards that is reshuffled and replenished after every draw.\n"
    "Entering an element a second or third time stacks the deck in that element's favour.\n"
    "Additionally, the algorithm accounts for differences in TS between elements, and adds more low TS units per draw of the deck.\n"
    "Each draw, the highest TS in the list is divided by the drawn element's TS. The quotient, dropping fractions, is how many of\n"
    "the drawn element will be added to the list.\n"
    "Ex. the 'Dragon' element has 15 TS, 'Archers' has 3 TS. Archer is drawn, 15/3 = 5, therefore 5 archers are added.\n"
    "This was done so that forces would not consist largely of powerful artillery or fantastical units.\n"
    "\n"
    "Writing your own .csv - if you have the ability to write .csv files (ex. with excel),\n"
    "then you can absolutely use files written outside of this program with it. Just remember to save it in\n"
    "the right place, and be careful with formatting. Using a text editor to copy/paste elements you wish to double up on\n"
    "or use from a previous army list is also likely to be easier than entering everything in this program\n"
    )

def doNothing():
    print("")

done = False
while done == False: 
    
    CurrentFile()

    try: 
        Select = int(input("What would you like to do?\n1 - New army\n2 - New element\n3 - Choose army .csv file\n4 - Build randomized army\n5 - Help\n6 - Exit\n"))
        if Select not in [1,2,3,4,5,6]:
            raise ValueError
    except ValueError:
        print("Please enter only intergers 1 through 6")
        Select = 7

    Menu = [NewArmy, NewElement, ChooseArmy, buildarmy, Tutorial, exit, doNothing]
    Menu[Select-1]()