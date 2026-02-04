from Shared.Data import UIModeData
from Utils import CustomInput

import os
# [Default, Text, TextOptions]

def ClearCLI():
    os.system('cls')

class new:
    def __init__(self):
        self.Prev = []
        self.Current = "Home"
        self.DefaultOption = "Return"
    
    def Start(self):
        ClearCLI()

        self.ComputeSelections()
        self.Display()

        # inp = CustomInput.Input('', {"Int": True}, "Include")
        self.WaitForContinuation()

        #TODO: find all choices in UIModeData.py, then call SystemManagerService to do the relevant functions

    def Next(self, idx):
        if self.Current == "Home" and self.Selections[idx] == "Return":
            self.WaitForContinuation()
            return

        ClearCLI()
        oldCurrent = self.Current

        self.Current = self.Selections[idx]
        if self.Current == "Return":
            self.Current = "Home" if not self.Prev else self.Prev.pop()

        node = UIModeData.Nodes[self.Current]

        success = False

        # if "PreExe" in node:
        #     success = node["PreExe"]()

        while not success and success != None:
            success = node["PreExe"]()
        
        if success == None:
            self.Current = "Home" if not self.Prev else self.Prev.pop()
            ClearCLI()

        self.ComputeSelections()
        self.Display()

        self.WaitForContinuation()

    def WaitForContinuation(self):
        inp = CustomInput.AwaitNumInputsBelow(len(self.Selections))
        self.Next(inp)
        
    def CreateTextFromOptions(self, array):
        AllModes = []

        for i in range(len(array) - 1):
            print(array[i + 1], "["+str(i + 1)+"]")
            AllModes.append(array[i + 1])

        if self.Current != "Home":
            print("Return [0]")

        return AllModes
    
    def ComputeSelections(self):
        optionText = UIModeData.Nodes[self.Current]["Text"]
        optionText = "Return, " + optionText

        self.Selections = optionText.split(", ")
    
    def Display(self): 
        AllModes = self.CreateTextFromOptions(self.Selections)     
        