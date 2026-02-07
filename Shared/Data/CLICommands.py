from Utils import CustomInput

Nodes = {}

def GetInputWithReturn(text, filterDict, filterMode):
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
    
    def GetEditAttributePreExe(propName, propDisplayName, filterDict, filterType):
        def anonymous():
            # This should never happen but just incase ykyk
            student = SystemManager.CurrentStudent
            if student == None: _findAStudentPreExe()

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
        
    def GetEditAttributePostExe(propName, propDisplayName):
        def anonymous(successData):
            student = SystemManager.CurrentStudent

            print(f"Successfully changed {propDisplayName} from {getattr(student, propName)} to {successData[propName]}!")
            student.Edit(propName, successData[propName])
            print(student)

        return anonymous

    def _displayStudentListPreExe():
        for student in SystemManager.Students:
            print(student)

        return ReturnSuccessRetry(True, False)

    Nodes = {
        "Home": {
            "Text": "Find A Student, Manage Students, Sort Scores, Display Student List",
        },

        "Find A Student": {
            "Text": "Find A Student, Edit Name, Edit Birth Year, Edit Major, Edit Scores",
            "PreExe": _findAStudentPreExe,
        },
        "Manage Students": {
            "Text": "Add, Edit, Delete",
        },
        "Sort Scores": {
            "Text": "Sort by ID, Sort by GPA, Sort by Name, Sort by Birth Year, Sort by Major",
        },
        "Display Student List": {
            "Text": "Find A Student",
            "PreExe": _displayStudentListPreExe,
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

        # Manage Students
        "Add": {
            "Text": "Normal Add, Quick Add",
        },
    }