

# settings
class RotorSetting:
    # are which rotors to put in + their positons
    def __init__(self,num,ringSetting):
        self.startingRotation = ringSetting
        self.number = num

class RotorSettings:
    # are which rotors to put in + their positons
    def __init__(self,rotorOne = 0,rotorTwo = 1,rotorThree = 2,rotorOneRotation = 4,rotorTwoRotation = 9,rotorThreeRotation = 15):
        self.rotorOne = RotorSetting(rotorOne,rotorOneRotation)
        self.rotorTwo = RotorSetting(rotorTwo,rotorTwoRotation)
        self.rotorThree = RotorSetting(rotorThree,rotorThreeRotation)

def ValidateListOfPlugs(plugs):
    letters = set()
    for plug in plugs:
        letters.add(plug.inputLetter)
        letters.add(plug.outputLetter)
    assert len(letters) == 20

def MakeDefaultListOfPlugs():
    plugs = []
    plug1 = Plug("a","z")
    plug2 = Plug("b","y")
    plug3 = Plug("c","x")
    plug4 = Plug("d","w")
    plug5 = Plug("e","v")
    plug6 = Plug("f","u")
    plug7 = Plug("g","t")
    plug8 = Plug("h","s")
    plug9 = Plug("i","r")
    plug10 = Plug("j","q")

    plugs.append(plug1)
    plugs.append(plug2)
    plugs.append(plug3)
    plugs.append(plug4)
    plugs.append(plug5)
    plugs.append(plug6)
    plugs.append(plug7)
    plugs.append(plug8)
    plugs.append(plug9)
    plugs.append(plug10)

    ValidateListOfPlugs(plugs)
    return plugs
# components

class Reflector:
    def __init__(self):
        self.Pathways = dict()
        self.InvertedPathways = dict()

        # create identity pathways, each letter is itself
        for letter,backwardsLetter in zip("ABCDEFGHIJKLMNOPQRSTUVWXYZ","IMETCGFRAYSQBZXWLHKDVUPOJN"):
            self.Pathways[letter] = backwardsLetter
            self.InvertedPathways[backwardsLetter] = letter
    
    def EncryptLetter(self,letter):
        return self.Pathways[letter]

    def DecryptLetter(self,letter):
        return self.InvertedPathways[letter]

class EntryWheel:
    def __init__(self):
        self.Pathways = dict()
        self.InvertedPathways = dict()

        # create identity pathways, each letter is itself
        for letter,backwardsLetter in zip("ABCDEFGHIJKLMNOPQRSTUVWXYZ","QWERTZUIOASDFGHJKPYXCVBNML"):
            self.Pathways[letter] = backwardsLetter
            self.InvertedPathways[backwardsLetter] = letter
    
    def EncryptLetter(self,letter):
        return self.Pathways[letter]

    def DecryptLetter(self,letter):
        return self.InvertedPathways[letter]


class Plug:
    def __init__(self,inputLetter,outputLetter):
        self.inputLetter = inputLetter
        self.outputLetter = outputLetter

class PlugBoard:
    def __init__(self,ListOfPlugs):
        self.Pathways = dict()
        self.InvertedPathways = dict()
        # create identity pathways, each letter is itself
        for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            self.Pathways[letter] = letter
            self.InvertedPathways[letter] = letter

        # overwrite the pathways for each plug and save inverse dict
        for plug in ListOfPlugs:
            inputLetter = str.upper(plug.inputLetter)
            outputLetter = str.upper(plug.outputLetter)
            
            # input goes to output
            self.Pathways[inputLetter] = outputLetter
            # output goes to input
            self.Pathways[outputLetter] = inputLetter
            # inverted for decrypting
            self.InvertedPathways[outputLetter] = inputLetter
            self.InvertedPathways[inputLetter] = outputLetter

    def EncryptLetter(self,letter):
        return self.Pathways[letter]

    def DecryptLetter(self,letter):
        return self.InvertedPathways[letter]
    


class Wiring:
    inputLetters="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    
    def __init__(self,num):
        """Creates a new wiring object

        Args:
            num (int): what wiring to choose from
        """
        self.name = num
        if num == 0:
            self.outputLetters="LPGSZMHAEOQKVXRFYBUTNICJDW"

        elif num == 1:
            self.outputLetters="SLVGBTFXJQOHEWIRZYAMKPCNDU"


        elif num == 2:
            self.outputLetters="CJGDPSHKTURAWZXFMYNQOBVLIE"


        elif num == 3:
            self.outputLetters="ESOVPZJAYQUIRHXLNFTGKDCMWB"

        elif num == 4:
            self.outputLetters="VZBRGITYUPSDNHLXAWMJQOFECK"
        # convert strings to arrays
        self.LettersToArrays()

        

    def LettersToArrays(self):
        """convert strings to arrays
        """
        inputLetters = list(self.inputLetters)
        outputLetters = list(self.outputLetters)
        self.inputLetters = inputLetters
        self.outputLetters = outputLetters

    

    def __str__(self):
        """when printing object, print the output letters array as string
        """
        return str(self.outputLetters)

    def EncryptLetter(self,letter,rotation):
        """Run a letter through the wiring with respect to the rotation of the rotor

        Args:
            letter (str): letter to run through rotor
            rotation (int): rotation 0-25 of the rotor

        Returns:
            str: encrypted letter
        """
        
        # find what letter of alphabet
        letterIndex = self.inputLetters.index(str.upper(letter))
        
        # add rotation into it
        letterIndex += rotation
        # if the index with rotation offset is greater than the max size, then subtract 26 to "roll over"
        if letterIndex>=26:
            letterIndex-=26
            
        
        # find letter in output
        outputLetter = self.outputLetters[letterIndex]
        
        #print(f"encrypting {letter} to {outputLetter} with rotation {rotation}")
        return outputLetter
    
    def DecryptLetter(self,letter,rotation):
        """Run letter through the rotor backwards

        Args:
            letter (str): letter to run through rotor
            rotation (int): rotation 0-25 of the rotor

        Returns:
            str: decrypted letter
        """
        # find index of our letter in ouput
        letterIndexInOutput = self.outputLetters.index(str.upper(letter))

        # subtract rotation 
        letterIndexInOutputMinusRotation = letterIndexInOutput - rotation
        # handle wrap around
        if letterIndexInOutputMinusRotation < 0:
            letterIndexInOutputMinusRotation = 26 + letterIndexInOutputMinusRotation
        # now have the output 1:1 letter for the input
        # find letter in input
        outputLetter = self.inputLetters[letterIndexInOutputMinusRotation]

        return outputLetter

class Rotor:
    

    def __str__(self):
        """prints status when object is called to be printed

        Returns:
            str: status of vars
        """
        Status = str(self.rotorPosition)
        Status += "\n"+str(self.notchPosition)
        return Status

    def __init__(self,num,startingRotation):
        """creates new Rotor object

        Args:
            num (int): which rotor to pick from of 0-4
        """
        self.name = num
        self.wiring = Wiring(num)
        self.wouldTurnNextRotor = False
        self.rotorPosition = startingRotation

        # notch positions based on rotor number
        if num == 0:
            self.notchPosition = 8
        elif num == 1:
            self.notchPosition = 8
        elif num == 2:
            self.notchPosition = 8
        elif num == 3:
            self.notchPosition = 11
        elif num == 4:
            self.notchPosition = 0

    def EncryptLetter(self,letter):
        """pass 

        Args:
            letter (_type_): _description_

        Returns:
            _type_: _description_
        """
        return self.wiring.EncryptLetter(letter,self.rotorPosition)
    def DecryptLetter(self,letter):
        
        return self.wiring.DecryptLetter(letter,self.rotorPosition)

    def Turn(self):
        self.rotorPosition+=1
        # count from 0 -> 25 if at 26 then is back to start
        if self.rotorPosition >=26:
            self.rotorPosition = 0
        
        # rotate if at notch
        self.wouldTurnNextRotor = (self.rotorPosition == self.notchPosition)

        #print(f"turning {self.name}")

class Enigma:

    rotorOne = None
    rotorTwo = None
    rotorThree = None
    
    def SetSettings(self,rotorSettings):
        """sets all settings from settings object

        Args:
            settings (EnigmaSettings): settings for the machine
        """
        # todo take all settings

        self.rotorOne = Rotor(rotorSettings.rotorOne.number, rotorSettings.rotorOne.startingRotation)
        self.rotorTwo = Rotor(rotorSettings.rotorTwo.number, rotorSettings.rotorTwo.startingRotation)
        self.rotorThree = Rotor(rotorSettings.rotorThree.number, rotorSettings.rotorThree.startingRotation)



        
    def __init__(self,rotorSettings,listOfPlugs):
        # set rotor settings
        self.SetSettings(rotorSettings)
        # create plugboard
        self.plugBoard = PlugBoard(listOfPlugs)
        # create entry wheel
        self.entry = EntryWheel()
        # create reflector
        self.reflector = Reflector()

    
    
    def Decrypt(self,toDecrypt,settings):
        """sets machine to starting settings then decrypts a string

        Args:
            toDecrypt (str): string to decrypt
            settings (EnigmaSettings): settings for decryption

        Returns:
            str: decrypted string
        """

        # set settings to settings
        self.SetSettings(settings)

        toDecrypt = str.upper(toDecrypt)
        # decrypt each letter
        outputString = ""
        for letter in toDecrypt:
            outputString+=self.DecryptLetter(letter)
        
        #print(outputString)
        return outputString
    
    def DecryptLetter(self,toDecrypt):
        """decrypts a letter

        Args:
            toDecrypt (str): string to decrypt

        Returns:
            str: decrypted character
        """


        outputLetter = toDecrypt

        # do entry wheel

        outputLetter = self.entry.DecryptLetter(outputLetter)


        # do plugboard
        
        outputLetter = self.plugBoard.DecryptLetter(outputLetter)
        #print(f"plugboard output for {toDecrypt} = {outputLetter}")
        #print("going through rotors")

        # rotate with each keypress
        self.Rotate()
        # go through rotors
        outputLetter = self.rotorOne.DecryptLetter(outputLetter)
        #print(outputLetter)
        outputLetter = self.rotorTwo.DecryptLetter(outputLetter)
        #print(outputLetter)
        #"""
        outputLetter = self.rotorThree.DecryptLetter(outputLetter)
        #print(outputLetter)
        # reflect
        outputLetter = self.reflector.DecryptLetter(outputLetter)
        # and back again
        outputLetter = self.rotorThree.DecryptLetter(outputLetter)
        #print(outputLetter)
        outputLetter = self.rotorTwo.DecryptLetter(outputLetter)
        #print(outputLetter)
        outputLetter = self.rotorOne.DecryptLetter(outputLetter)
        #print(outputLetter)
        #"""
        #print("gone through rotors")


        # do plugboard
        rotoredLetter = outputLetter
        outputLetter = self.plugBoard.DecryptLetter(outputLetter)
        #print(f"plugboard output for {rotoredLetter} = {outputLetter}")
        
        # do entrywheel
        outputLetter = self.entry.DecryptLetter(outputLetter)


        return outputLetter
    
    # encrypt
    def Encrypt(self,toEncrypt):

        toEncrypt = str.upper(toEncrypt)

        outputString = ""
        for letter in toEncrypt:
            outputString+=self.EncryptLetter(letter)
        
        #print(outputString)
        return outputString

    def EncryptLetter(self,toEncrypt):
        outputLetter = toEncrypt
        #print("encrypting")
        # entry wheel
        outputLetter = self.entry.EncryptLetter(outputLetter)

        # do plugboard
        outputLetter = self.plugBoard.EncryptLetter(outputLetter)
        #print(f"plugboard output for {toEncrypt} = {outputLetter}")
        # rotate with each keypress
        self.Rotate()
        # go through rotors
        #print("going through rotors")

        outputLetter = self.rotorOne.EncryptLetter(outputLetter)
        
        #"""
        
        #print(outputLetter)
        outputLetter = self.rotorTwo.EncryptLetter(outputLetter)
        #print(outputLetter)
        outputLetter = self.rotorThree.EncryptLetter(outputLetter)
        #print(outputLetter)
        # reflect
        outputLetter = self.reflector.EncryptLetter(outputLetter)
        # and back again
        outputLetter = self.rotorThree.EncryptLetter(outputLetter)
        #print(outputLetter)
        outputLetter = self.rotorTwo.EncryptLetter(outputLetter)
        #print(outputLetter)
        outputLetter = self.rotorOne.EncryptLetter(outputLetter)
        #print(outputLetter)
        #"""
        #print("gone through rotors")

        
        rotoredLetter = outputLetter
        # do plugboard
        outputLetter = self.plugBoard.EncryptLetter(outputLetter)
        #print(f"plugboard output for {rotoredLetter} = {outputLetter}")
        # entry wheel
        outputLetter = self.entry.EncryptLetter(outputLetter)
        if outputLetter == toEncrypt:
            print("error! letter to self")
            

        return outputLetter
    
    def Rotate(self):
        # turn all the rotors
        self.rotorOne.Turn()
        if self.rotorOne.wouldTurnNextRotor:
            self.rotorTwo.Turn()
        if self.rotorTwo.wouldTurnNextRotor:
            self.rotorThree.Turn()
        #print(self.rotorOne.rotorPosition,self.rotorOne.wouldTurnNextRotor)
        #print(self.rotorOne.rotorPosition)




# start code

test = 0

if test ==0:
    # check that pushing a 27 times = different all times and doesnt roll back to same
    
    
    rotors = RotorSettings()
    plugs = MakeDefaultListOfPlugs()
    Machine = Enigma(rotors,plugs)

    # TODO figure out how its getting a as an output when its an input
    toEncrypt = "hello world"
    toEncrypt = "a"
    for i in range(278):
        print(i)
        print(Machine.Encrypt(toEncrypt))

elif test == 1:
    # test decryption
    
    rotors = RotorSettings()
    plugs = MakeDefaultListOfPlugs()
    Machine = Enigma(rotors,plugs)

    toEncrypt = "helloworld"
    #toEncrypt = "a"
    encrypted = Machine.Encrypt(toEncrypt)
    print("encrypted",toEncrypt,"to", encrypted)

    # decrypt
    decrypted = Machine.Decrypt(encrypted,rotors)
    print("decrypted",encrypted,"to", decrypted)
elif test ==2:


    plugs = MakeDefaultListOfPlugs()
    board = PlugBoard(plugs)
    for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        outputLetter = board.EncryptLetter(letter)
        print(f"{letter}->{outputLetter}")


