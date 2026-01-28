from Classes import StudentObject
from Classes import ScoresObject

from Services import SystemManagerService

SystemManager = SystemManagerService.new()

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
                [1] = ID
                [2] = Name
                [3] = BirthYear
                [4] = Major
                [5..n] = Subjects' Scores
            """
            subjectScores = {}
            for j in range(len(subjects)):
                subjectScores[subjects[j]] = words[j + 4]
            
            scores = ScoresObject.new(subjectScores)
            student = StudentObject.new(words[0], words[1], words[2], words[3], scores)
            print(student)
            
            