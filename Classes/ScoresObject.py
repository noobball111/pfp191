from typing import Callable, Any

class Scores:
    def __init__(self, subjects: dict[str, int]):
        self._subjects = subjects
        
    def SetChangedCallback(self, func: Callable[..., Any]):
        # This function will run whenever Edit successfully ran (basically when a score is changed, useful for binding this with CalculateGPA so it refreshes with every edit)
        self._onChangedCallback = func
        
    def Edit(self, subject: str, value: int):
        # Check if the subject exists
        if self._subjects[subject] != int:
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
        