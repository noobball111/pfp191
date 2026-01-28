from UIControllerData import UIModeData

class new:
    def __init__(self):
        self.Prev = []
        self.Cur = "Home"
        self.DefaultOption = "Return"
        self.ModeText = UIModeData[1]
    
    def Start(self):
        
    def Display(self, Mode):
        AllModes = None
        if Mode == "Home":
            Selections = self.ModeText[Mode].split(", ")
            AllModes = CreateFromOptions(Selections)
        
        self.Cur = AllModes[]
            
    def CreateFromOptions(array):
        AllModes = []
        for i in range(len(array)):
            print(array[i], "["+str(i)+"]")
            AllModes.append(array[i])
        return AllModes
        