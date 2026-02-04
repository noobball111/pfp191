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
    
    def _editNamePreExe():
        # This should never happen but just incase ykyk
        student = SystemManager.CurrentStudent
        if student == None: _findAStudentPreExe()

        print("Type \"/r | /return\" to go back at any time...")
        print(f"You are editting student [{student.ID}] - {student.Name}'s Name...")

        # newName = CustomInput.Input(f"Please enter {student.Name}'s new name: ", {"Int": True, "Float": True}, "Exclude") 
        newName = GetInputWithReturn(f"Please enter {student.Name}'s new name: ", {"Int": True, "Float": True}, "Exclude") 
        if newName == "/r": return ReturnSuccessRetry(False, False)

        print(f"Are you sure you want to change {student.Name} to {newName}? [Y/N]")

        # key = CustomInput.Input("", {"Int": True, "Float": True}, "Exclude") 
        key = GetInputWithReturn("", {"Int": True, "Float": True}, "Exclude") 
        
        successData = ReturnSuccessRetry(True, key.lower() != 'y')
        successData["NewName"] = newName

        return successData

        # if key.lower() != "y":
        #     _editNamePreExe()
        #     return
        
        
        # print(f"Successfully changed {student.Name} to {newName}!")
        # student.Edit("Name", newName)
        # print(student)

        # return True

    def _editNamePostExe(successData):
        student = SystemManager.CurrentStudent

        print(f"Successfully changed {successData["NewName"]} to {successData["NewName"]}!")
        student.Edit("Name", successData["NewName"])
        print(student)

    def _displayStudentListPreExe():
        for student in SystemManager.Students:
            print(student)

        return ReturnSuccessRetry(True, False)

    Nodes = {
        "Home": {
            "Text": "Find A Student, Manage students, Sort Scores, Display Student List",
        },
        "Find A Student": {
            "Text": "Find A Student, Edit Name, Edit Birth Year, Edit Major, Edit Scores",
            "PreExe": _findAStudentPreExe,
        },
        "Manage Students": {
            "Text": "Add, Edit, Delete",
        },
        "Add": {
            "Text": "Normal Add, Quick Add",
        },
        "Display Student List": {
            "Text": "Find A Student",
            "PreExe": _displayStudentListPreExe,
        },
        "Sort Scores": {
            "Text": "Sort by ID, Sort by GPA, Sort by Name, Sort by Birth Year, Sort by Major",
        },
        "Edit Name": {
            "Text": "",
            "PreExe": _editNamePreExe,
            "PostExe": _editNamePostExe,
        }
    }