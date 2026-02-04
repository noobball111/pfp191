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
        isReturnCMD = self.Current == "Return"

        if isReturnCMD:
            self.Current = "Home" if not self.Prev else self.Prev.pop()

        node = UIModeData.Nodes[self.Current]
        # Only execute if found the PreExe function of the node (nodes like Home won't have any so just skip)
        if "PreExe" in node:
            successData = UIModeData.ReturnSuccessRetry(False, True)

            while successData["Retry"]:
                successData = node["PreExe"]()
            
            if not successData["Success"]:
                self.Current = "Home" if not self.Prev else self.Prev.pop()
                ClearCLI()
            else:
                if "PostExe" in node: node["PostExe"](successData)
                # It's 2 steps behind but it's better UX wise I think
                if not isReturnCMD:
                    self.Prev.append(oldCurrent)


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
        optionText = UIModeData.Nodes[self.Current]["Text"]
        if len(optionText) >= 1:
            optionText = "Return, " + optionText
        else:
            optionText = "Return"

        self.Selections = optionText.split(", ")
    
    def Display(self): 
        self.CreateTextFromOptions(self.Selections)     
        