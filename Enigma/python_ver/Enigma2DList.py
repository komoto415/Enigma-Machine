import re


class Rotor:

    def __init__(self, wiring):
        self.wiring = wiring
        self.position = 0

    def rotate(self):
        self.position += 1
        if(self.position == 26):
            self.position = 0

    def encipher(self, send, direction):
        if direction:
            send = (send + self.position) % 26
            output = self.wiring[send][1]
            return output
        if not direction:
            for i in range(26):
                if send == self.wiring[i][1]:
                    output = (self.wiring[i][0] - self.position)
                    while (output < 0):
                        output = output + 26
                    output = output % 26
                    return output

    def __str__(self):
        return str(self.wiring)


class PlugBoard:

    def __init__(self, connections):
        self.connections = connections
    
    def encipher(self, send, direction):
        if send in list(self.connections.keys()) and direction:
            return self.connections[send]
        elif send in list(self.connections.values()) and not direction:
            for key, value in self.connections.items():
                if value == send:
                    return key
        return send       


def main():
    global alphabet, encipher
    alphabet = getSubstitutions('alphabet')

    print(' _____________________________ ')
    print('|   __     __     __     __   |')
    print('|  |  | < |  | < |  | < |  |  |')
    print('|  |rf|   |r1|   |r2|   |r3|  |')
    print('|  |__| > |__| > |__| > |__|  |')
    print('|  Q W E R T Y U I O P    bck |')
    print('|   A S D F G H J K L    entr |')
    print('|    Z X C V B N M       nope |')
    print('|_____________________________|')

    applyInputs()
    retString = ""

    # print(len(encipher))
    for i in range(len(encipher)):
        if encipher[i] == ' ':
            retString += ''
        else:
            retString += numIndexToChar(execute(i))
    print(retString)


def applyInputs():
    global encipher, rotorThr, rotorTwo, rotorOne, reflc, plugBrd
    inputs = getSettings()

    encipher = inputs[0]
    rotors = inputs[1]
    positions = inputs[2]
    reflc = inputs[3]
    plugBrd = inputs[4]

#     print()
#     print(encipher)
#     print(rotors)
#     print(positions)
#     print(reflc)
#     print()

    for i in range(len(encipher)):
        encipher[i] = charToNumIndex(encipher[i])

    rotorThr = numberToRotor(int(rotors[2]))
    rotorTwo = numberToRotor(int(rotors[1]))
    rotorOne = numberToRotor(int(rotors[0]))

    rotorThr.position = int(positions[2])
    rotorTwo.position = int(positions[1])
    rotorOne.position = int(positions[0])

    reflc = numberToReflc(reflc)
    
    plugBrd = PlugBoard(plugBrd)


def getSettings():
    validInput = False
    while not validInput:
        encipher = input("\nWhat do you want to encrypt? ")
        validInput = (re.match("[A-Z]", encipher.strip()))
        if not validInput:
            print('no goo')
    encipher = list(encipher.replace(" ", "").upper())

    validInput = False
    while not validInput:
        print("\nThe order you type them will be represented as in the image above")
        print("Example: 2 3 1 --> r1 r2 r3")
        print("Available rotors: 1, 2, 3, 4, 5")
        rotors = input("What rotors do you want to use? ")
        validInput = re.match("^[1-3] [1-3] [1-3]$", rotors.strip())
        if not validInput:
            print('no goo')
        else:
            rotors = rotors.strip().split(" ")
            validInput = not (rotors[0] == rotors[1] or rotors[1] == rotors[2] or rotors[0] == rotors[2])
            if not validInput:
                print('no goo')

    validInput = False
    while not validInput:
        print("\nValid positions are between 0 and 26 inclusive")
        positions = input("What position do you want to start at? ")
        validInput = re.match("^[0-26] [0-26] [0-26]$", positions.strip())
        if not validInput:
            print('no goo')
    positions = positions.strip().split(" ")

    validInput = False
    while not validInput:
        print("\nAvailable reflectors: 1, 2")
        reflc = int(input("What reflector would you like to use? "))
        validInput = reflc == 1 or reflc == 2
        if not validInput:
            print('no goo')
    
    validInput = False
    while not validInput:
        plugBrd = input("\nWhat plug board connections do you wants? ")
        validInput = re.match("^([A-Z]{2})( [A-Z]{2})*", plugBrd.strip())
        if not validInput:
            print('no goo')
    plugBrd = list(plugBrd.split(" "))
    plugBrdDict = {}
    for i in range(len(plugBrd)):
        plugBrd[i] = list(plugBrd[i])
        plugBrdDict[charToNumIndex(plugBrd[i][0])] = charToNumIndex(plugBrd[i][1])
    
    return [encipher, rotors, positions, reflc, plugBrdDict]


def execute(index):
    global encipher, rotorThr, rotorTwo, rotorOne, reflc, plugBrd
    
    encipherLetter = encipher[index]
    encipherLetter = plugBrd.encipher(encipherLetter, True)
    encipherLetter = rotorThr.encipher(encipherLetter, True)
    encipherLetter = rotorTwo.encipher(encipherLetter, True)
    encipherLetter = rotorOne.encipher(encipherLetter, True)
    encipherLetter = reflc.encipher(encipherLetter, True)
    encipherLetter = rotorOne.encipher(encipherLetter, False)
    encipherLetter = rotorTwo.encipher(encipherLetter, False)
    encipherLetter = rotorThr.encipher(encipherLetter, False)
    encipherLetter = plugBrd.encipher(encipherLetter, False)
    
    moveRotors()
    return encipherLetter


def moveRotors():
    global rotorThr, rotorTwo, rotorOne
    rotorThr.rotate()
    if rotorThr.position == 26:
        rotorThr.position = 0
        rotorTwo.rotate()
    if (rotorTwo.position == 26):
        rotorTwo.setPosition = 0
        rotorOne.rotate()
    if rotorOne.position == 26:
        rotorOne.position = 0


def charToNumIndex(char):
    return ord(char.upper()) - 65


def numIndexToChar(num):
    return chr(num + 65)


def numberToRotor(rotorNum):
    switch = {
        1: Rotor(makeList([], getSubstitutions('rotorAlpha'))),
        2: Rotor(makeList([], getSubstitutions('rotorBeta'))),
        3: Rotor(makeList([], getSubstitutions('rotorCharlie'))),
        4: Rotor(makeList([], getSubstitutions('rotorDelta'))),
        5: Rotor(makeList([], getSubstitutions('rotorEpsilon'))),
        }
    return switch.get(rotorNum, "nothing")


def numberToReflc(reflcNum):
    switch = {
        1: Rotor(makeList([], getSubstitutions('reflectorAlpha'))),
        2: Rotor(makeList([], getSubstitutions('reflectorBeta'))),
        }
    return switch.get(reflcNum, "nothing")


def makeList(myList, subs):
    global alphabet
    for i in range(26):
        myList.append([alphabet[i], subs[i]])
    return myList


def getSubstitutions(sub):
    textFile = '../' + sub + '.txt'
    with open(textFile, 'r') as subFile:
        subFile = list(subFile.readline().rstrip('\n'))
        for i in range(len(subFile)):
            subFile[i] = charToNumIndex(subFile[i])
        return (subFile)


main()
