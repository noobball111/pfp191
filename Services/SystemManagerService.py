from Shared.SignalBank import SignalBank
from Utils import CustomInput

class new:
    def __init__(self):
        self.Students = []
        self.LookupStudents = {}
        self._lastSortKey = "ID" 

        SignalBank.SystemManagerCalled.Connect(self.All)

    def All(self, WorkType, *args):
        if WorkType == "Add":
            self.AddStudent(args)
        elif WorkType == "EditFromName":
            Name, Subject, Value = args

            students = self.FromName(Name)

            students[0].Edit(subject, value)
            #TODO: allow user to choose 1 student using UIController.py
        elif WorkType == "EditFromID":
            student = self.FromID(args)
            subject = CustomInput.Input(f"Enter subject to change: ")
            value = CustomInput.Input("Enter value: ")

            student.Edit(subject, value)
            # def Input(Text, FilterList = {}, FilterType = None, RetryUntilValid = True):
        elif WorkType == "Delete":
            delType, value = args
            
            if delType == "ID":
                self.DeleteStudentFromID(value)
            elif delType == "Name":
                students = self.FromName(value)
                #TODO: allow to choose 1 from many using UICOntroller
                   
                student = students[0]

                if not student: return "Cannot find"

                self.DeleteStudentFromID(student.ID)


            

    def AddStudent(self, student):
        if self.FromID(student.ID):
            print("Duplicated ID")
            return
        
        self.Students.append(student)
        self.LookupStudents[student.ID] = student
        
    def FromID(self, ID):
        # if self.LookupStudents[ID] == None: return
        if not ID in self.LookupStudents: return
        return self.LookupStudents[ID]
    
    def FromName(self, Name):
        chosenStudents = []
        for student in self.Students:
            if student.Name != Name: continue
            chosenStudents.append(student)
            
        return chosenStudents
    
    def FromIDOrName(self, IDorName):
        student = self.FromID(IDorName)
        if student == None:
            student = self.FromName(IDorName)
            if len(student) <= 0:
                # Student doesn't exist so redo the func
                return None, None
            else:
                # GG now its a list
                return student, "Name"
        else:
            # Found student by ID (only 1)
            return student, "ID"
        
    def DeleteStudentFromID(self, ID):
        # chosenStudent = self.LookupStudents[ID]
        if not ID in self.LookupStudents: return

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
    
        