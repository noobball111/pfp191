from Shared.Data import CLICommands
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

        #TODO: find all choices in CLICommands.py, then call SystemManagerService to do the relevant functions

    def Next(self, idx):
        if self.Current == "Home" and self.Selections[idx] == "Return":
            self.WaitForContinuation()
            return

        ClearCLI()
        oldCurrent = self.Current

        self.Current = self.Selections[idx]
        isReturnCMD = self.Current == "Return"

        if isReturnCMD:
            self.Current = "Home" if not self.Prev else self.Prev.pop()
        else:
            self.Prev.append(oldCurrent)

        node = CLICommands.Nodes[self.Current]
        # Only execute if found the PreExe function of the node (nodes like Home won't have any so just skip)
        # If found PreExe then PostExe can only run after PreExe fulfill the conditions
        # Otherwise PostExe can run standalone
        if "PreExe" in node:
            successData = CLICommands.ReturnSuccessRetry(False, True)

            while successData["Retry"]:
                successData = node["PreExe"]()
            
            if not successData["Success"]:
                self.Current = "Home" if not self.Prev else self.Prev.pop()
                ClearCLI()
            else:
                if "PostExe" in node: node["PostExe"](successData)

                # if not isReturnCMD:
                #     self.Prev.append(self.Current)
        else:
            # Since there's no "PreExe", there's no success data for commands with only PostExe
            if "PostExe" in node: node["PostExe"]()
            print("did post exe")


        self.ComputeSelections()
        self.Display()

        self.WaitForContinuation()

    def WaitForContinuation(self):
        inp = CustomInput.AwaitNumInputsBelow(len(self.Selections))
        self.Next(inp)
        
    def CreateTextFromOptions(self, array):
        # AllModes = []

        # print("Array length: ", len(array))

        for i in range(len(array) - 1):
            print(array[i + 1], "["+str(i + 1)+"]")
            # AllModes.append(array[i + 1])

        if self.Current != "Home":
            print("Return [0]")

        # return AllModes
    
    def ComputeSelections(self):
        optionText = CLICommands.Nodes[self.Current]["Text"]
        if len(optionText) >= 1:
            optionText = "Return, " + optionText
        else:
            optionText = "Return"

        self.Selections = optionText.split(", ")
    
    def Display(self): 
        self.CreateTextFromOptions(self.Selections)     
        