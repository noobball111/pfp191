class new:
    def __init__(self, ID, Name, BirthYear, Major, Scores):
        self.ID = ID
        self.Name = Name
        self.BirthYear = BirthYear
        self.Major = Major
        self.Scores = Scores
        self._IDVerificationFunc = True
        
    def __str__(self):
        return f'My ID: {self.ID}, Name: {self.Name}, Born in {self.BirthYear}, Major: {self.Major}'
        
        
    def Edit(self, key, value):
        if key == "ID" and self._IDVerificationFunc != None:
            if self._IDVerificationFunc(value):
                return false
            
        self[key] = value
        return true
    
    def Display(self):
        print(self.ID, self.Name)
    