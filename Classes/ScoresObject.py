from typing import Callable, Any

class new:
    def __init__(self, subjects: dict[str, int]):
        self._subjects = subjects
        
    def SetChangedCallback(self, func: Callable[..., Any]):
        self._onChangedCallback = func
        
    def Edit(self, subject: str, value: int):
        if self._subjects[subject] != int:
            print("No valid subject for", subject)
            return
        
        self._subjects[subject] = value
        if self._onChangedCallback != None:
            self._onChangedCallback(subject, value)
        
    def CalculateGPA(self):
        res = 0
        for x in self._subjects.values():
            res += x
            
        return res / len(self._subjects)
        