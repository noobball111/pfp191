from typing import Callable, Any

class Scores:
    def __init__(self, subjects: dict[str, float]):
        self._subjects = subjects
        
    def SetChangedCallback(self, func: Callable[..., Any]):
        # This function will run whenever Edit successfully ran (basically when a score is changed, useful for binding this with CalculateGPA so it refreshes with every edit)
        # Yes, this is a band-aid solution without a module like Signal
        self._onChangedCallback = func
        
    def Get(self, subject: str):
        return self._subjects[subject]

    def Edit(self, subject: str, value: float):
        # Check if the subject exists
        if type(self._subjects[subject]) is not float:
            print("No valid subject for", subject)
            return
        
        self._subjects[subject] = value
        if self._onChangedCallback != None:
            self._onChangedCallback(subject, value)
        
    def CalculateGPA(self):
        # Loop through everything and then divide it by the length to find the average value which is the GPA
        res = 0
        for x in self._subjects.values():
            res += x
            
        return res / len(self._subjects)
        