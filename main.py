from Classes import StudentObject
from Classes import ScoresObject

from Services import SystemManagerService
from Services import UIController

from Utils.Signal import Signal
from Utils import CustomInput

from Shared.Data import UIModeData

SystemManager = SystemManagerService.new()
UIModeData.Init(SystemManager)

CLI = UIController.new()

subjectAmount = 0
subjects = []



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