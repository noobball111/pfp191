from Shared.Data import UIModeData
from Utils import CustomInput

import os
# [Default, Text, TextOptions]

def ClearCLI():
    os.system('cls')

class new:
    def __init__(self):
        self.Prev = []
        self.Cur = "Home"
        self.DefaultOption = "Return"
        self.ModeText = UIModeData.Text
    
    def Start(self):
        #Add loop
        
        ClearCLI()
        self.Prev.append(self.Cur)
        self.Display(self.Cur)

        # inp = CustomInput.Input('', {"Int": True}, "Include")
        inp = CustomInput.AwaitNumInputsBelow(3)
        ClearCLI()
        print("Chosen ", inp)

        #TODO: find all choices in UIModeData.py, then call SystemManagerService to do the relevant functions
        
    def CreateTextFromOptions(self, array):
        AllModes = []
        for i in range(len(array)):
            print(array[i], "["+str(i)+"]")
            AllModes.append(array[i])
        return AllModes
    
    def Display(self, Mode):
        AllModes = None
        if Mode == "Home":
            Selections = self.ModeText[Mode]["Text"].split(", ")
            AllModes = self.CreateTextFromOptions(Selections)
        
        # inp = CustomInput.Input("> ", {"Int": True}, "Include")

        # self.Cur = AllModes[inp]        
        