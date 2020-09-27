import re


class Rotor:

    def __init__(self, wiring):
        self.wiring = wiring
        self.position = 0

    def rotate(self):
        self.position += 1

    def encipher(self, send, direction):
        send = numIndexToChar((charToNumIndex(send) + self.position) % 26)
        if direction:
            return self.wiring[send]
        elif not direction:
            for key, value in self.wiring.items():
                if value == send:
                    return key

    def __repr__(self):
        return f'Rotor({self.wiring})'

    def __str__(self):
        return f'''Substitution: {self.wiring}
                Current Rotor Position: {self.position}
                '''


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

    def __repr__(self):
        return f'PlugBoard({self.connections})'

    def __str__(self):
        return f'Substitution: {self.connections}'


class Machine:

    def __init__(self, reflector, rotorOne, rotorTwo, rotorThr, plugBrd):
        self.reflector = reflector
        self.rotorOne = rotorOne
        self.rotorTwo = rotorTwo
        self.rotorThr = rotorThr
        self.plugBrd = plugBrd

    def __repr__(self):
        return f'Machine({self.reflector}, {self.rotorOne}, {self.rotorTwo}, {self.rotorThr}, {self.plugBrd}'

    def __str__(self):
        return f'''My Machine Settings:
                Reflector: {self.reflector}
                Rotor One: {self.rotorOne}
                Rotor Two: {self.rotorTwo}
                Rotor Three: {self.rotorThr}
                Plug Board: {self.plugBrd}
                '''


def main():
    global alphabet
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
    print()

    print("Lets determine your board settings first!")
    menu = True
    while menu:
        machine = applyInputs()
        if machine == '':
            menu = False
        else:
            validInput = False
            while not validInput:
                message = input("\nWhat do you want to encrypt? ")
                message = message.strip()
                validInput = (re.match("[A-Z]", message))
                if message == '':
                    validInput = True
                elif not validInput:
                    print('no goo')
                else:
                    message = list(message.replace(" ", "").upper())
                    encryptedMessage = execute(machine, message)
                    print(encryptedMessage)
                keepGoing = input("Would you like to continue?: ")
                validInput = not re.match("^Y$", keepGoing.upper().strip())
            menu = False

    print("Program has ended")


def applyInputs():
    settings = getSettings()
    myMachine = settings
    if myMachine != '':
        rotors = settings[0]
        positions = settings[1]
        reflc = settings[2]
        plugBrd = settings[3]

        reflect = numberToReflc(reflc)

        rotorThr = numberToRotor(int(rotors[2]))
        rotorTwo = numberToRotor(int(rotors[1]))
        rotorOne = numberToRotor(int(rotors[0]))

        rotorThr.position = int(positions[2])
        rotorTwo.position = int(positions[1])
        rotorOne.position = int(positions[0])

        plugBrd = PlugBoard(plugBrd)

        myMachine = Machine(reflect, rotorOne, rotorTwo, rotorThr, plugBrd)

    return myMachine


def getSettings():

    validInput = False
    while not validInput:
        print("\nThe order you type them will be represented as in the image above")
        print("Example: 2 3 1 --> r1 r2 r3")
        print("Available rotors: 1, 2, 3, 4, 5")
        print("Hit enter if you no longer want to use the machine")
        rotors = input("What rotors do you want to use? ")
        validInput = re.match("^[1-5] [1-5] [1-5]$", rotors.strip())
        if rotors.strip() == '':
            return ''
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
        print("Just use 0 0 0 for now")
        positions = input("What three position do you want to start at? ")
        validInput = re.match("^[0-9]|1[0-9]|2[0-6] [0-9]|1[0-9]|2[0-6] [0-9]|1[0-9]|2[0-6]$", positions.strip())
        if not validInput:
            print('no goo')
    positions = positions.strip().split(" ")

    validInput = False
    while not validInput:
        print("\nAvailable reflectors: 1, 2")
        reflector = int(input("What reflector would you like to use? "))
        validInput = reflector == 1 or reflector == 2
        if not validInput:
            print('no goo')

    validInput = False
    while not validInput:
        plugBrd = input("\nWhat plug board connections do you wants? ")
        plugBrd = plugBrd.lstrip()
        validInput = re.match("^([A-Z]{2} ){,10}$", (plugBrd + ' '))
        if not validInput:
            print('no goo')
        else:
            keys = list(filter(lambda index, value: index % 3 == 0, enumerate(plugBrd)))
            values = list(filter(lambda index, value: index % 3 == 1, enumerate(plugBrd)))
            any_in = lambda a, b: bool(set(keys).intersection(values))
            validInput = len(set(keys)) == len(set(values)) and not any_in
            if not validInput:
                print('no goo')
    plugBrdDict = {}
    for index, key in enumerate(keys):
        plugBrdDict[key] = values[index]

    return [rotors, positions, reflector, plugBrdDict]


def execute(myMachine, message):
    retString = ""
    for index, _ in enumerate(message):
        encipherLetter = message[index]
        if encipherLetter == " ":
            retString += " "
        else:
            encipherLetter = myMachine.plugBrd.encipher(encipherLetter, True)
            encipherLetter = myMachine.rotorThr.encipher(encipherLetter, True)
            encipherLetter = myMachine.rotorTwo.encipher(encipherLetter, True)
            encipherLetter = myMachine.rotorOne.encipher(encipherLetter, True)
            encipherLetter = myMachine.reflector.encipher(encipherLetter, True)
            encipherLetter = myMachine.rotorOne.encipher(encipherLetter, False)
            encipherLetter = myMachine.rotorTwo.encipher(encipherLetter, False)
            encipherLetter = myMachine.rotorThr.encipher(encipherLetter, False)
            encipherLetter = myMachine.plugBrd.encipher(encipherLetter, False)
            retString += encipherLetter
        moveRotors(myMachine)

    return retString


    # Doesn't quite work at all. Well, rotations are fine, it just isn't effecting the
    # encrypting process
def moveRotors(myMachine):
    myMachine.rotorThr.rotate()
    if myMachine.rotorThr.position == 26:
        myMachine.rotorThr.position = 0
        myMachine.rotorTwo.rotate()
    if (myMachine.rotorTwo.position == 26):
        myMachine.rotorTwo.setPosition = 0
        myMachine.rotorOne.rotate()
    if myMachine.rotorOne.position == 26:
        myMachine.rotorOne.position = 0


def numberToRotor(rotorNum):
    switch = {
        1: Rotor(makeDict(getSubstitutions('rotorAlpha'))),
        2: Rotor(makeDict(getSubstitutions('rotorBeta'))),
        3: Rotor(makeDict(getSubstitutions('rotorCharlie'))),
        4: Rotor(makeDict(getSubstitutions('rotorDelta'))),
        5: Rotor(makeDict(getSubstitutions('rotorEpsilon'))),
        }
    return switch.get(rotorNum, "nothing")


def numberToReflc(reflcNum):
    switch = {
        1: Rotor(makeDict(getSubstitutions('reflectorAlpha'))),
        2: Rotor(makeDict(getSubstitutions('reflectorBeta'))),
        }
    return switch.get(reflcNum, "nothing")


def makeDict(subs):
    global alphabet
    myDict = {}
    for i in range(26):
        myDict[alphabet[i]] = subs[i]
    return myDict


def charToNumIndex(char):
    return ord(char.upper()) - 65


def numIndexToChar(num):
    return chr(num + 65)


def getSubstitutions(sub):
    textFile = '../' + sub + '.txt'
    with open(textFile, 'r') as subFile:
        subFile = list(subFile.readline().rstrip('\n'))
        for i, _ in enumerate(subFile):
            subFile[i] = subFile[i]
        return (subFile)


main()
