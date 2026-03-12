from typing import Any, Callable
from Classes.ScoresObject import Scores

class Student:
    def __init__(self, ID: str, Name: str, BirthYear: int, Major: str, Scores: Scores):
        self.ID = ID
        self.Name = Name
        self.BirthYear = BirthYear
        self.Major = Major
        self.Scores = Scores
        self.GPA = Scores.CalculateGPA()

        # Whenever any score is changed, the GPA instantly updates
        def setGPA(_a, _b):
            self.GPA = Scores.CalculateGPA()

        Scores.SetChangedCallback(setGPA)
        
    def __str__(self):
        return f'[{self.ID}] {self.Name} - GPA: {self.GPA:.2f} | Born in {self.BirthYear}, Major: {self.Major}.'
    
    def Edit(self, key: str, value: Any):
        # ID Duplication is already done in the command
        setattr(self, key, value)
    
    def Display(self):
        # Display everything
        print(f"[ID]: {self.ID}")
        print(f"[Name]: {self.Name}")
        print(f"[Birth Year]: {self.BirthYear}")
        print(f"[Major]: {self.Major}")
        print("--------- Scores ---------")
        print(f"[GPA]: {self.GPA}")

        for subject, score in getattr(self.Scores, "_subjects").items():
            print(f"[{subject}'s Score]: {score}")