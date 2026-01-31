from Shared.SignalBank import SignalBank

class new:
    def __init__(self):
        self.Students = []
        self.LookupStudents = {}
        self._lastSortKey = "ID"

        SignalBank.SystemManagerCalled.Connect(self.All)

    def All(self, WorkType, *args):
        if WorkType == "Add":
            self.AddStudent(args)

    def AddStudent(self, student):
        if self.FromID(student.ID):
            print("Duplicated ID")
            return
        
        self.Students.append(student)
        self.LookupStudents[student.ID] = student
        
    def FromID(self, ID):
        if self.LookupStudents[ID] == None: return
        return self.LookupStudents[ID]
    
    def FromName(self, Name):
        chosenStudents = []
        for student in self.Students:
            if student.Name != Name: continue
            chosenStudents.append(student)
            
        return chosenStudents
    
    def DeleteStudentFromID(self, ID):
        chosenStudent = self.LookupStudents[ID]
        if chosenStudent == None: return
        
        self.Students.remove(chosenStudent)
        del self.LookupStudents[ID]
        
    def SortBy(self, key):
        self._lastSortKey = key
        self.Students.sort(key=lambda student : student[key])
        
    def DisplayScores(self):
        for student in self.Students:
            print(f'ID: {student.ID} | Name: {student.Name} | Birth Year: {student.BirthYear} | Major: {student.Major}')
            for subject, score in student.Scores._subjects.items():
                print(f'[{subject}]: {score}')
    
        