from Classes import StudentObject
from Classes import ScoresObject

from Services import SystemManagerService
from Services import UIController

from Utils.Signal import Signal
from Utils import CustomInput

from Shared.Data import UIModeData

SystemManager = SystemManagerService.new()
CLI = UIController.new()

subjectAmount = 0
subjects = []

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

UIModeData.Nodes["Search"]["PreExe"] = _searchPreExe

with open("SaveData.txt") as f:
    i = 0
    for line in f:
        i += 1
        words = line.split(',')
        
        if i == 1:
            # Subjects
            subjectAmount = len(words)
            
            for w in words:
                subjects.append(w)
        else:
            """
                [0] = ID
                [1] = Name
                [2] = BirthYear
                [3] = Major
                [4..n] = Subjects' Scores
            """
            subjectScores = {}
            for j in range(len(subjects)):
                subjectScores[subjects[j]] = words[j + 4]
            
            scores = ScoresObject.new(subjectScores)
            student = StudentObject.new(words[0], words[1], words[2], words[3], scores)

            SystemManager.AddStudent(student)

CLI.Start()