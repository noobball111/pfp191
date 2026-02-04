from Utils import CustomInput

Nodes = {}

def GetInputWithReturn(text, filterDict, filterMode):
    oup = CustomInput.Input(text, filterDict, filterMode)
    # TODO: If not string then just return output (or is this always string idk)

    if oup.lower() == "/r" or oup.lower() == "/return":
        return "/r"
    return oup


def Init(SystemManager):
    global Nodes

    def _searchPreExe():
        print("Type \"/r | /return\" to go back at any time...")

        student = None
        getType = None
        while student == None:
            IDorName = GetInputWithReturn("Enter Student's ID/Name: ", {"Int": True, "Float": True}, "Exclude")
            if IDorName == "/r": return None, None

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
                if ID == "/r": return None, None
                
                student = SystemManager.FromID(ID)

                while student == None:
                    ID = GetInputWithReturn("Enter the right ID please: ", {"Int": True, "Float": True}, "Exclude") 
                    if ID == "/r": return None, None

                    student = SystemManager.FromID(ID)

                print(f"Found student by ID: [{student.ID}] {student.Name}")

        SystemManager.CurrentStudent = student

        return student == None and False or True, student
    
    def _editNamePreExe():
        # This should never happen but just incase ykyk
        student = SystemManager.CurrentStudent
        if student == None: _searchPreExe()

        print("Type \"/r | /return\" to go back at any time...")
        print(f"You are editting student [{student.ID}] - {student.Name}'s Name...")

        # newName = CustomInput.Input(f"Please enter {student.Name}'s new name: ", {"Int": True, "Float": True}, "Exclude") 
        newName = GetInputWithReturn(f"Please enter {student.Name}'s new name: ", {"Int": True, "Float": True}, "Exclude") 
        if newName == "/r": return None, None

        print(f"Are you sure you want to change {student.Name} to {newName}? [Y/N]")

        # key = CustomInput.Input("", {"Int": True, "Float": True}, "Exclude") 
        key = GetInputWithReturn("", {"Int": True, "Float": True}, "Exclude") 
        if key == "/r": return None, None


        if key.lower() != "y":
            _editNamePreExe()
            return
        
        
        print(f"Successfully changed {student.Name} to {newName}!")
        student.Edit("Name", newName)
        print(student)

        return True

    Nodes = {
        "Home": {
            "Text": "Search, Manage students, Sort Scores",
        },
        "Search": {
            "Text": "Edit Name, Edit Birth Year, Edit Major, Edit Scores",
            "PreExe": _searchPreExe,
        },
        "Manage Students": {
            "Text": "Add, Edit, Delete",
        },
        "Add": {
            "Text": "Normal Add, Quick Add",
        },
        "Sort Scores": {
            "Text": "Sort by ID, Sort by GPA, Sort by Name, Sort by Birth Year, Sort by Major",
        },
        "Edit Name": {
            "Text": "",
            "PreExe": _editNamePreExe,
        }
    }