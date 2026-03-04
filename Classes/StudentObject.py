from typing import Any, Callable
from Classes.ScoresObject import Scores

class Student:
    def __init__(self, ID: str, Name: str, BirthYear: int, Major: str, Scores: Scores):
        self.ID = ID
        self.Name = Name
        self.BirthYear = BirthYear
        self.Major = Major
        self.Scores = Scores
        # Not used as of right now, was drafted in during planning process, may not need anymore.
        self._IDVerificationFunc: Callable[..., str]
        
    def __str__(self):
        return f'[{self.ID}] {self.Name}, Born in {self.BirthYear}, Major: {self.Major}'
    
    def Edit(self, key: str, value: Any):
        #If editting the ID then do an extra check to see if that ID is a duplicate
        # Not used as of right now
        if key == "ID" and self._IDVerificationFunc != None:
            if self._IDVerificationFunc(value):
                return False
        
        setattr(self, key, value)
        return True
    
    def Display(self):
        print(self.ID, self.Name)