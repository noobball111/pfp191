class Student: 
    def __init__(self, ID, Name, BirthYear, Major, Scores):
        self.ID = ID
        self.Name = Name
        self.BirthYear = BirthYear
        self.Major = Major
        self.Scores = Scores
        self._IDVerificationFunc = True
        
    def __str__(self):
        return f'[{self.ID}] {self.Name}, Born in {self.BirthYear}, Major: {self.Major}'
        
    def new(self, *args):
        return Student(self, args)

    def Edit(self, key, value):
        if key == "ID" and self._IDVerificationFunc != None:
            if self._IDVerificationFunc(value):
                return False
        
        setattr(self, key, value)
        return True
    
    def Display(self):
        print(self.ID, self.Name)