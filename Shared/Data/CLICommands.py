from Classes.StudentObject import Student
from Classes.ScoresObject import Scores

from Utils import CustomInput

Nodes = {}
# This script is just hard coded commands

def GetInputWithReturn(text: str, filterDict: dict[str, bool], filterMode: str):
    oup = CustomInput.Input(text, filterDict, filterMode)
    # TODO: If not string then just return output (or is this always string idk)

    if oup.lower() == "/r" or oup.lower() == "/return":
        return "/r"
    return oup

def ReturnSuccessRetry(success, retry):
    # Success: True when function completed without /r, False if /r is used
    # Retry: True when you want to retry (like re-entering name), False if you want to end it right there
    # Retry should only be false when it is /r, otherwise the data won't be validated and bug the whole program

    return {
            "Success": success,
            "Retry": retry,
        }


def Init(SystemManager):
    global Nodes

    def _findAStudentPreExe():
        print("Type \"/r | /return\" to go back at any time...")

        student = None
        getType = None
        while student == None:
            IDorName = GetInputWithReturn("Enter Student's ID/Name: ", {"Int": True, "Float": True}, "Exclude")
            if IDorName == "/r": return ReturnSuccessRetry(False, False)

            student, getType = SystemManager.FromIDOrName(IDorName)

        if getType == "ID":
            print(f"Found student by ID: [{student.ID}] {student.Name}")
        else:
            # Name
            if len(student) <= 1:
                # Only 1
                print("Get type: ", getType)
                student = student[0]
                print(f"Found student by Name: [{student.ID}] {student.Name}")
            else:
                # More than 1
                print(f"Found {len(student)} Students in the Database: ")
                for person in student:
                    print(person)
                print("-------------------------------------")

                ID = GetInputWithReturn("Please enter the desired ID: ", {"Int": True, "Float": True}, "Exclude")
                if ID == "/r": return ReturnSuccessRetry(False, False)
                
                student = SystemManager.FromID(ID)

                while student == None:
                    ID = GetInputWithReturn("Enter the right ID please: ", {"Int": True, "Float": True}, "Exclude") 
                    if ID == "/r": return ReturnSuccessRetry(False, False)

                    student = SystemManager.FromID(ID)

                print(f"Found student by ID: [{student.ID}] {student.Name}")

        if student != None:
            SystemManager.CurrentStudent = student
            return ReturnSuccessRetry(True, False)
        else:
            return ReturnSuccessRetry(True, True)
        
    def TryToFindCurrentStudent():
        student = getattr(SystemManager, "CurrentStudent", None)
        if student == None:
            findSuccessData = ReturnSuccessRetry(True, True)
            while findSuccessData["Retry"]:
                findSuccessData = _findAStudentPreExe()
                
            # Update the var incase it found a student
            student = getattr(SystemManager, "CurrentStudent", None)
            if student == None: return ReturnSuccessRetry(False, False), None

        return ReturnSuccessRetry(True, False), student
    
    def GetEditAttributePreExe(propName, propDisplayName, filterDict, filterType):
        def anonymous():
            findSuccessData, student = TryToFindCurrentStudent()
            if student == None: return findSuccessData

            print("Type \"/r | /return\" to go back at any time...")
            print(f"You are editting student [{student.ID}] - {getattr(student, "Name")}'s {propName}...")

            studentProp = getattr(student, propName)

            newPropVal = GetInputWithReturn(f"Please enter {getattr(student, "Name")}'s new {propDisplayName}: ", filterDict, filterType) 
            if newPropVal == "/r": return ReturnSuccessRetry(False, False)

            print(f"Are you sure you want to change {studentProp} to {newPropVal}? [Y/N]")

            key = GetInputWithReturn("", {"Int": True, "Float": True}, "Exclude") 
            
            successData = ReturnSuccessRetry(True, key.lower() != 'y')
            successData[propName] = newPropVal

            return successData

        return anonymous

    def GetEditAttributePostExe(propName: str, propDisplayName: str):
        def anonymous(successData):
            student = SystemManager.CurrentStudent

            print(f"Successfully changed {propDisplayName} from {getattr(student, propName)} to {successData[propName]}!")
            student.Edit(propName, successData[propName])
            print(student)

        return anonymous
    
    def _normalAddPreExe():
        print("Type \"/r | /return\" to go back at any time...")

        id = GetInputWithReturn("Enter Student's ID: ", {"Float": True}, "Exclude")
        if id == "/r": return ReturnSuccessRetry(False, False)

        name = GetInputWithReturn("Enter Student's Name: ", {"Int": True, "Float": True}, "Exclude")
        if name == "/r": return ReturnSuccessRetry(False, False)

        birthYear = GetInputWithReturn("Enter Student's Birth Year: ", {"Int": True}, "Include")
        if birthYear == "/r": return ReturnSuccessRetry(False, False)

        major = GetInputWithReturn("Enter Student's Major: ", {"Int": True, "Float": True}, "Exclude")
        if major == "/r": return ReturnSuccessRetry(False, False)

        # Declare a dictionary (key = subject's name | value = the score)
        subjectScores = {}
        subjectText = ""
        for subject in SystemManager.SubjectList:
            subjectScores[subject] = float(GetInputWithReturn(f"Enter {subject}'s Score: ", {"Int": True, "Float": True}, "Include"))
            subjectText += f"\n[{subject}'s Score]: {subjectScores[subject]}"

        print(
        f"""Are you sure you want to add a new student with this info? [Y/N]
[ID]: {id}
[Name]: {name}
[Birth Year]: {birthYear}
[Major]: {major}{subjectText}
        """)

        key = GetInputWithReturn("", {"Int": True, "Float": True}, "Exclude") 
        
        successData = ReturnSuccessRetry(True, key.lower() != 'y')
        successData["ID"] = id
        successData["Name"] = name
        successData["BirthYear"] = birthYear
        successData["Major"] = major
        successData["Scores"] = subjectScores

        return successData

    def _quickAddPreExe():
        print("Type \"/r | /return\" to go back at any time...")
        subjectText = ""
        for subject in SystemManager.SubjectList:
            subjectText += f",{subject}'s Score"

        print("Enter the student's info in the following format:")

        fullInfo = GetInputWithReturn(f"ID,Name,Birth Year,Major{subjectText}\n", {"Int": True, "Float": True}, "Exclude")
        if fullInfo == "/r": return ReturnSuccessRetry(False, False)

        while len(fullInfo.split(',')) != 4 + len(SystemManager.SubjectList):
            print(len(fullInfo.split(',')))
            print(4 + len(SystemManager.SubjectList))
            print("Invalid number of inputs, please retry:")
            fullInfo = GetInputWithReturn(f"ID,Name,Birth Year,Major{subjectText}\n", {"Int": True, "Float": True}, "Exclude")
            if fullInfo == "/r": return ReturnSuccessRetry(False, False)


        data = fullInfo.split(',')

        # Declare a dictionary (key = subject's name | value = the score)
        subjectScores = {}
        subjectText = ""

        # TODO: (Optional) Type check the data so scores cant be string, and birth year cant be string

        for i in range(4, len(data)):
            subject = SystemManager.SubjectList[i - 4]

            subjectScores[subject] = float(data[i])
            subjectText += f"\n[{subject}'s Score]: {subjectScores[subject]}"

        print(
        f"""Are you sure you want to add a new student with this info? [Y/N]
[ID]: {data[0]}
[Name]: {data[1]}
[Birth Year]: {data[2]}
[Major]: {data[3]}{subjectText}
        """)

        key = GetInputWithReturn("", {"Int": True, "Float": True}, "Exclude") 
        
        successData = ReturnSuccessRetry(True, key.lower() != 'y')
        successData["ID"] = data[0]
        successData["Name"] = data[1]
        successData["BirthYear"] = data[2]
        successData["Major"] = data[3]
        successData["Scores"] = subjectScores

        return successData

    def _addPostExe(successData) -> None:
        newStudent = Student(successData["ID"], successData["Name"], successData["BirthYear"], successData["Major"], Scores(successData["Scores"]))
        success = SystemManager.AddStudent(newStudent)

        if success:
            print(f"Successfully added [{successData["ID"]}] {successData["Name"]} to the Database!")
            print(newStudent)
        else:
            print(f"ID [{successData["ID"]}] is already in the database, please enter a valid ID.")

    def _editScoresPreExe():
        student = SystemManager.CurrentStudent

        subjectScores = {}
        subjectText = ""

        for subject in SystemManager.SubjectList:
            subjectScores[subject] = float(GetInputWithReturn(f"Enter {subject}'s Score: ", {"Int": True, "Float": True}, "Include"))
            subjectText += f"[{subject}'s Score]: {student.Scores.Get(subject)} -> {subjectScores[subject]}\n"

        print(f"Are you sure you want to change [{student.ID}] {student.Name} to: [Y/N]\n{subjectText}")
        
        key = GetInputWithReturn("", {"Int": True, "Float": True}, "Exclude") 
        
        successData = ReturnSuccessRetry(True, key.lower() != 'y')
        successData["Scores"] = subjectScores

        return successData

    def _editScoresPostExe(successData):
        student = SystemManager.CurrentStudent

        for subject, score in successData["Scores"].items():
            student.Scores.Edit(subject, score)

        print(f"Successfully changed [{student.ID}] {student.Name}'s Scores!")
        print(student)


    def _displayStudentListPostExe():
        for student in SystemManager.Students:
            print(student)

        return ReturnSuccessRetry(True, False)

    # def GenerateID() -> str:
    #     # return "SE21"+str(len(SystemManager.Students))
    #     return "dsjahdjadhkuas"

    def _deleteStudentPreExe():
        # This should never happen but just incase ykyk
        findSuccessData, student = TryToFindCurrentStudent()
        if student == None: return findSuccessData

        print(f"Are you sure you want to delete the student [{student.ID}] - {student.Name}? [Y/N]")

        key = GetInputWithReturn("", {"Int": True, "Float": True}, "Exclude") 
        if key.lower() != 'y':
            # Return them back
            return ReturnSuccessRetry(False, False)

        SystemManager.DeleteStudentFromID(student.ID)
        SystemManager.CurrentStudent = None

        successData = ReturnSuccessRetry(True, False)
        successData["DeletedStudent"] = student

        return successData

    def _deleteStudentPostExe(successData):
        print(f"Successfully deleted student [{successData["DeletedStudent"].ID}] - {successData["DeletedStudent"].Name}")

    def GetSortPreExe(sortType):
        def anonymous():
            isReverse = sortType == "GPA"
            SystemManager.Students = sorted(SystemManager.Students, key=lambda student: getattr(student, sortType), reverse=isReverse)
            return ReturnSuccessRetry(True, False)

        return anonymous

    def GetSortPostExe(sortType):
        def anonymous(successData):
            _displayStudentListPostExe()
            print(f"Successfully sorted Students by {sortType}!")

        return anonymous
    
    def exist():
        return
    

        return anonymous

    Nodes = {
        "Home": {
            "Text": "Find A Student, Manage Students, Sort Scores, Display Student List, Exit",
        },

        # #Exist
        # "Exist": {
        #     "Text": "",
        #     "PostExe": exist()
        # },

        "Find A Student": {
            "Text": "Find A Student, Edit Name, Edit Birth Year, Edit Major, Edit Scores, Delete The Student",
            "PreExe": _findAStudentPreExe,
        },
        "Manage Students": {
            "Text": "Add A Student, Edit A Student, Delete A Student",
        },
        "Sort Scores": {
            "Text": "Sort by ID, Sort by GPA, Sort by Name, Sort by Birth Year, Sort by Major",
        },
        "Display Student List": {
            "Text": "Find A Student",
            "PostExe": _displayStudentListPostExe,
        },

        # Find A Student
        "Edit Name": {
            "Text": "",
            "PreExe": GetEditAttributePreExe("Name", "Name", {"Int": True, "Float": True}, "Exclude"),
            "PostExe": GetEditAttributePostExe("Name", "Name"),
        },
        "Edit Birth Year": {
            "Text": "",
            "PreExe": GetEditAttributePreExe("BirthYear", "Birth Year", {"Int": True}, "Include"),
            "PostExe": GetEditAttributePostExe("BirthYear", "Birth Year"),
        },
        "Edit Major": {
            "Text": "",
            "PreExe": GetEditAttributePreExe("Major", "Major", {"Int": True, "Float": True}, "Exclude"),
            "PostExe": GetEditAttributePostExe("Major", "Major"),
        },
        "Edit Scores": {
            "Text": "",
            "PreExe": _editScoresPreExe,
            "PostExe": _editScoresPostExe,
        },
        "Delete The Student": {
            "Text": "",
            "PreExe": _deleteStudentPreExe,
            "PostExe": _deleteStudentPostExe,
        },

        # Manage Students
        "Add A Student": {
            "Text": "Normal Add, Quick Add",
        },
        "Normal Add": {
            "Text": "Normal Add, Quick Add",
            "PreExe": _normalAddPreExe,
            "PostExe": _addPostExe,
        },
        "Quick Add": {
            "Text": "Normal Add, Quick Add",
            "PreExe": _quickAddPreExe,
            "PostExe": _addPostExe,
        },

        "NewIDMode":{
            "Text": "Auto, Manual"
        },
        "Auto ID":{
            "Text": "",
            "PreExe": print()
        },
        "Manual ID": {
            "Text": "",
            "PreExe": print()
        },

        "Edit A Student": {
            "Text": "Find A Student, Edit Name, Edit Birth Year, Edit Major, Edit Scores, Delete The Student",
            "PreExe": _findAStudentPreExe,
        },

        "Delete A Student": {
            "Text": "",
            "PreExe": _deleteStudentPreExe,
            "PostExe": _deleteStudentPostExe,
        },
        
        #Sort by ID, Sort by GPA, Sort by Name, Sort by Birth Year, Sort by Major
        "Sort by ID": {
            "Text": "Edit A Student, Sort by GPA, Sort by Name, Sort by Birth Year, Sort by Major",
            "PreExe": GetSortPreExe("ID"),
            "PostExe": GetSortPostExe("ID"),
        },

        "Sort by GPA": {
            "Text": "Edit A Student, Sort by ID, Sort by Name, Sort by Birth Year, Sort by Major",
            "PreExe": GetSortPreExe("GPA"),
            "PostExe": GetSortPostExe("GPA"),
        },

        "Sort by Name": {
            "Text": "Edit A Student, Sort by ID, Sort by GPA, Sort by Birth Year, Sort by Major",
            "PreExe": GetSortPreExe("Name"),
            "PostExe": GetSortPostExe("Name"),
        },

        "Sort by Birth Year": {
            "Text": "Edit A Student, Sort by ID, Sort by GPA, Sort by Name, Sort by Major",
            "PreExe": GetSortPreExe("BirthYear"),
            "PostExe": GetSortPostExe("BirthYear"),
        },

        "Sort by Major": {
            "Text": "Edit A Student, Sort by ID, Sort by GPA, Sort by Name, Sort by Birth Year",
            "PreExe": GetSortPreExe("Major"),
            "PostExe": GetSortPostExe("Major"),
        },
    }