from Utils import CustomInput

Nodes = {}

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

    def GetEditAttributePostExe(propName: str, propDisplayName: str) -> function:
        def anonymous(successData):
            student = SystemManager.CurrentStudent

            print(f"Successfully changed {propDisplayName} from {getattr(student, propName)} to {successData[propName]}!")
            student.Edit(propName, successData[propName])
            print(student)

        return anonymous
    
    def GetNormalAddPreExe():
        print("Type \"/r | /return\" to go back at any time...")

        Name = GetInputWithReturn("Enter Student's Name: ", {"Int": True, "Float": True}, "Exclude")
        if Name == "/r": return ReturnSuccessRetry(False, False)

        print("")

    def GetNormalAddPostExe() -> None:
        pass


    def _displayStudentListPostExe():
        for student in SystemManager.Students:
            print(student)

        return ReturnSuccessRetry(True, False)

    # def GenerateID() -> str:
    #     # return "SE21"+str(len(SystemManager.Students))
    #     return "dsjahdjadhkuas"

    def _editScoresPreExe():
        # TODO: Display all subjects in alphabetical order, then let the user choose the subject in question
        pass

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

    Nodes = {
        "Home": {
            "Text": "Find A Student, Manage Students, Sort Scores, Display Student List",
        },

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
        # "Edit Scores": {
        #     "Text": "",
        #     "PreExe": _editNamePreExe,
        #     "PostExe": _editNamePostExe,
        # },
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
            "Text": "",
            "PreExe": ""
        },
        "Quick Add": {

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

        "Delete A Student": {
            "Text": "",
            "PreExe": _deleteStudentPreExe,
            "PostExe": _deleteStudentPostExe,
        },
    }