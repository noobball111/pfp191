from ..Shared.Data.UIModeData import UIModeData
from ..Utils import CustomInput

# [Default, Text, TextOptions]

class new:
    def __init__(self):
        self.Prev = []
        self.Cur = "Home"
        self.DefaultOption = "Return"
        self.ModeText = UIModeData[1]
    
    def Start(self):
        #Add loop
        
        self.Prev.append(self.Cur)
        self.Display(self.Cur)
        
        #TODO: find all choices in UIModeData.py, then call SystemManagerService to do the relevant functions
        
    def CreateTextFromOptions(array):
        AllModes = []
        for i in range(len(array)):
            print(array[i], "["+str(i)+"]")
            AllModes.append(array[i])
        return AllModes
    
    def Display(self, Mode):
        AllModes = None
        if Mode == "Home":
            Selections = self.ModeText[Mode].split(", ")
            AllModes = CreateTextFromOptions(Selections)
        
        self.Cur = AllModes[CustomInput.Input("", {"Int": True}, "Include")]
            
        
