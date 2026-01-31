from Utils import CustomInput

Nodes = {}

def Init(SystemManager):
    global Nodes

    def _searchPreExe():
        student = None
        getType = None
        while student == None:
            IDorName = CustomInput.Input("Enter Student's ID/Name: ", {"Int": True, "Float": True}, "Exclude") 
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

                ID = CustomInput.Input("Please enter the desired ID: ", {"Int": True, "Float": True}, "Exclude") 
                student = SystemManager.FromID(ID)

                while student == None:
                    ID = CustomInput.Input("Enter the right ID please: ", {"Int": True, "Float": True}, "Exclude") 
                    student = SystemManager.FromID(ID)

                print(f"Found student by ID: [{student.ID}] {student.Name}")

        SystemManager.CurrentStudent = student

        return True, student

    Nodes = {
        "Home": {
            "Text": "Search, Manage students, Sort Scores",
        },
        "Search": {
            "Text": "Edit Name, Edit Birth Year, Edit Major, Edit Scores",
            "PreExe": _searchPreExe
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
            "Text": ""
        }
    }