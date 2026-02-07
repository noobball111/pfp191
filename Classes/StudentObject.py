from typing import Any, Callable

class Student:
    def __init__(self, ID: str, Name: str, BirthYear: int, Major: str, Scores: dict[str, int]):
        _IDVerificationFunc: bool

        self.ID = ID
        self.Name = Name
        self.BirthYear = BirthYear
        self.Major = Major
        self.Scores = Scores
        self._IDVerificationFunc: Callable[..., str]
        
    def __str__(self):
        return f'[{self.ID}] {self.Name}, Born in {self.BirthYear}, Major: {self.Major}'
        
    def Edit(self, key: str, value: Any):
        if key == "ID" and self._IDVerificationFunc != None:
            if self._IDVerificationFunc(value):
                return False
        
        setattr(self, key, value)
        return True
    
    def Display(self):
        print(self.ID, self.Name)