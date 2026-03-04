from Shared.SignalBank import SignalBank
from Utils import CustomInput

class new:
    # Initialization of SystemManager
    def __init__(self):
        # Declare Students as a list
        # LookupStudents as a dictionary for ease of looking up
        # _lastSortKey is a private variable, used for knowing the current way the data is sorted in (If "ID" then the data is sorted by ID now)
        self.Students = []
        self.LookupStudents = {}

        self.SubjectList = []

        self._lastSortKey = "ID" 

    #     SignalBank.SystemManagerCalled.Connect(self.All)

    # def All(self, WorkType, *args):
    #     if WorkType == "Add":
    #         self.AddStudent(args)
    #     elif WorkType == "EditFromName":
    #         Name, Subject, Value = args

    #         students = self.FromName(Name)

    #         students[0].Edit(subject, value)
    #         #TODO: allow user to choose 1 student using UIController.py
    #     elif WorkType == "EditFromID":
    #         student = self.FromID(args)
    #         subject = CustomInput.Input(f"Enter subject to change: ")
    #         value = CustomInput.Input("Enter value: ")

    #         student.Edit(subject, value)
    #         # def Input(Text, FilterList = {}, FilterType = None, RetryUntilValid = True):
    #     elif WorkType == "Delete":
    #         delType, value = args
            
    #         if delType == "ID":
    #             self.DeleteStudentFromID(value)
    #         elif delType == "Name":
    #             students = self.FromName(value)
    #             #TODO: allow to choose 1 from many using UICOntroller
                   
    #             student = students[0]

    #             if not student: return "Cannot find"

    #             self.DeleteStudentFromID(student.ID)

    def AddStudent(self, student):
        # print(student)
        # Check if there's a duplicated ID
        if self.FromID(student.ID):
            print("Duplicated ID")
            return
        
        # If no duplicated ID then add the student to the Students list, and listing their ID as the key for LookupStudents
        self.Students.append(student)
        self.LookupStudents[student.ID] = student

    def GetStudents(self):
        return self.Students
        
    def FromID(self, ID):
        # if self.LookupStudents[ID] == None: return
        # if ID not found in LookupStudents then the student with that ID doesn't exist
        if not ID in self.LookupStudents: return
        return self.LookupStudents[ID]
    
    def FromName(self, Name):
        # Returns a list of possible students with that Name
        chosenStudents = []
        for student in self.Students:
            # Check if the student name matches with the name from the input
            if student.Name != Name: continue
            chosenStudents.append(student)
            
        return chosenStudents
    
    def FromIDOrName(self, IDorName):
        # FromID + FromName
        # Check if it's possible to find from the ID first, if not then check for Name
        student = self.FromID(IDorName)
        if student == None:
            student = self.FromName(IDorName)
            if len(student) <= 0:
                # Student doesn't exist so redo the func
                return None, None
            else:
                # This returns a list and the way it was found
                return student, "Name"
        else:
            # Found student by ID (only 1)
            # This returns a student and the way it was found
            return student, "ID"
        
    def DeleteStudentFromID(self, ID):
        # chosenStudent = self.LookupStudents[ID]
        # if ID not found in LookupStudents then the student with that ID doesn't exist
        if not ID in self.LookupStudents: return

        chosenStudent = self.LookupStudents[ID]
        
        # Remove the student with the ID from both Students (list) and LookupStudents (dictionary)
        self.Students.remove(chosenStudent)
        del self.LookupStudents[ID]
        
    def SortBy(self, key):
        # Sort the Students list based on the key from the input (ID, Name, BirthYear, etc...)

        self._lastSortKey = key
        self.Students.sort(key=lambda student : student[key])
        
    def DisplayScores(self):
        # Display all the students in the Students list
        for student in self.Students:
            print(f'ID: {student.ID} | Name: {student.Name} | Birth Year: {student.BirthYear} | Major: {student.Major}')
            for subject, score in student.Scores._subjects.items():
                print(f'[{subject}]: {score}')
    
        