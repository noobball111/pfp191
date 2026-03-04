# Importing Classes, Services and Util modules

from Classes.StudentObject import Student
from Classes.ScoresObject import Scores

from Services import SystemManagerService
from Services import UIController

from Utils.Signal import Signal
from Utils import CustomInput

from Shared.Data import CLICommands

# Create a new SystemManager
SystemManager = SystemManagerService.new()
# Initialize the console commands by passing in the SystemManager so it has a reference
CLICommands.Init(SystemManager)

# Create a new Console/UIController object
CLI = UIController.new()

# Declare 2 variables for subject amount and a list/collection of subjects
subjectAmount = 0
subjects = []

# Open SaveData.txt as f
with open("SaveData.txt") as f:
    # Declare i 
    i = 0
    # Loop through each line in f (SaveData.txt)
    for line in f:
        # Increment i
        i += 1
        # Remove \n from the line
        line = line.replace("\n", "")

        # Declare words as a list/collection by separating with ',' from the file
        words = line.split(',')
        # print(words)
        if i == 1:
            # i == 1 because the first line is just for registering subjects
            # the number of subjects is defined by the length of the list/collection words we listed above
            # Example: "Math,Biology,Science" is going to give words as [Math, Biology, Science], which has 3 elements so the length is 3
            subjectAmount = len(words)
            
            # Loop through every word in word and add it to the empty subject list
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

            # Declare a dictionary (key = subject's name | value = the score)
            subjectScores = {}
            for j in range(len(subjects)):
                # subjects[j] = the subject name
                # words[j + 4] = the score, because the first 4 elements are ID, Name, BirthYear and Major
                subjectScores[subjects[j]] = words[j + 4]
            
            # Create a new scores object from the subjectScores dictionary
            scores = Scores(subjectScores)
            # Create a new student object from their ID, Name, BirthYear, Major and the scores object just created above
            student = Student(words[0], words[1], int(words[2]), words[3], scores)

            # Add the student to the SystemManager to easily manage students
            SystemManager.AddStudent(student)
            # print(student, subjectScores)
    # print(SystemManager.GetStudents())

            # Set SystemManager's subjectlist to the subjects found.
            SystemManager.SubjectList = subjects

# Start the Console Interface
# CLI.Start()


def Serialize(data):
    scores = data.Scores._subjects

    return f'{data.ID},{data.Name},{data.BirthYear},{data.Major},{scores["Math"]},{scores["Physics"]},{scores["PE"]},{scores["Geography"]}\n'

def save(path):
    f = open(path, "w")

    # print(SystemManager.Students)

    # Math,Physics,PE,Geography
    f.write("Math,Physics,PE,Geography\n")
    for student in SystemManager.GetStudents():
        print(student.Scores._subjects)
        f.write(Serialize(student))
    
    f.close()

save("SaveData.txt")