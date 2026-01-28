class new:
    def __init__(self, subjects):
        self._subjects = subjects
        
    def SetChangedCallback(self, func):
        self._onChangedCallback = func
        
    def Edit(self, subject, value):
        if self._subjects[subject] == None:
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
        