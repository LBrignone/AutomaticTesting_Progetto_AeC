import random
import string
from datetime import date
from ElementGen import *
from DateDurationCalc import calculateSecondDate

def generateSubPatternProfOrg (*elements):
    localProfessorId = elements[0].copy()
    j = 0
    subPattern = ''
    for i in elements[4]:
        regular = random.choice(localProfessorId)
        localProfessorId.remove(regular)
        verId = generateVersion(j, 0)
        j += 1
        if i == 0:
            if elements[5] == 0:
                subPattern = '[{' + regular + ',' + verId + ',['
            else:
                idRegularChoice = random.choice(['', regular])
                idVersionChoice = random.choice(['', verId])
                subPattern = '[{' + idRegularChoice + ',' + idVersionChoice + ',['
        else:
            if elements[5] == 0:
                subPattern = subPattern + '{' + regular + ',' + verId + ',['
            else:
                idRegularChoice = random.choice(['', regular])
                idVersionChoice = random.choice(['', verId])
                subPattern = subPattern + '{' + idRegularChoice + ',' + idVersionChoice + ',['
        lessonHVer = elements[1]
        exerciHVer = elements[2]
        laboraHVer = elements[3]
        lessonHV = 0
        exerciHV = 0
        laboraHV = 0
        k = 0
        while lessonHVer != 0 or exerciHVer != 0 or laboraHVer != 0:
            if k == 0:
                while lessonHV == 0 and exerciHV == 0 and laboraHV == 0:
                    lessonHV = random.randint(0, lessonHVer)
                    exerciHV = random.randint(0, exerciHVer)
                    laboraHV = random.randint(0, laboraHVer)
                if elements[5] == 0:
                    subPattern = subPattern + '{' + regular + ',' + str(lessonHV) + ',' + str(exerciHV) + ',' + str(laboraHV) + '}'
                else:
                    idRegularChoice = random.choice(['', regular])
                    lessonHChoice = random.choice(['', str(lessonHV)])
                    exerciseHChoice = random.choice(['', str(exerciHV)])
                    labHChoice = random.choice(['', str(laboraHV)])
                    subPattern = subPattern + '{' + idRegularChoice + ',' + lessonHChoice + ',' + exerciseHChoice + ',' + labHChoice + '}'
            else:
                professor = random.choice(localProfessorId)
                localProfessorId.remove(professor)
                if lessonHVer > 5:
                    lessonHV = random.randint(0, lessonHVer)
                else:
                    lessonHV = lessonHVer
                if exerciHVer > 5:
                    exerciHV = random.randint(0, exerciHVer)
                else:
                    exerciHV = exerciHVer
                if laboraHVer > 5:
                    laboraHV = random.randint(0, laboraHVer)
                else:
                    laboraHV = laboraHVer
                if lessonHV != 0 or exerciHV != 0 or laboraHV != 0:
                    if elements[5] == 0:
                        subPattern = subPattern + ',{' + professor + ',' + str(lessonHV) + ',' + str(exerciHV) + ',' + str(laboraHV) + '}'
                    else:
                        if k < int(elements[6][i]):
                            idRegularChoice = random.choice(['', professor])
                        else:
                            idRegularChoice = professor
                        lessonHChoice = random.choice(['', str(lessonHV)])
                        exerciseHChoice = random.choice(['', str(exerciHV)])
                        labHChoice = random.choice(['', str(laboraHV)])
                        subPattern = subPattern + ',{' + idRegularChoice + ',' + lessonHChoice + ',' + exerciseHChoice + ',' + labHChoice + '}'
            k += 1
            lessonHVer = lessonHVer - lessonHV
            exerciHVer = exerciHVer - exerciHV
            laboraHVer = laboraHVer - laboraHV
        subPattern = subPattern + ']}'
        if i == elements[4][-1]:
            subPattern = subPattern + ']'
        else:
            subPattern = subPattern + ','
    return subPattern

def generateSubPatternExamOrg():
    examH = random.randrange(60, 240, 10)
    entrance = random.randrange(5, 15, 5)
    exit = random.randrange(5, 15, 5)
    partecipants = random.randint(1, 400)
    clTy = random.choice(['A', 'L'])
    exTy = random.choice(['S', 'O', 'SO', 'P'])
    subPattern = '{' + str(examH) + ',' + str(entrance) + ',' + str(exit) + ',' + exTy + ',' + clTy + ',' + str(partecipants) + '}'
    return subPattern

def generateSubPatternGroupedCourses(coursesGen, courseGiven):
    val1 = int(coursesGen)
    val2 = int(courseGiven)
    courses = ''
    groupedCour = range(random.randint(1, 6))
    coursesId = generateCourseIdList(val1)
    coursesId.remove(coursesId[val2])
    for l in groupedCour:
        courseChosen = random.choice(coursesId)
        coursesId.remove(courseChosen)
        if l == 0:
            if l == groupedCour[-1]:
                courses = '{}'
            else:
                courses = '{' + courseChosen
        elif l == groupedCour[-1]:
            courses = courses + ',' + courseChosen + '}'
        else:
            courses = courses + ',' + courseChosen
    return courses

def generateEndedCourses ():
    endedCourses = ''
    endedCO = range(random.randint(0, 6))
    for x in endedCO:
        if x == 0:
            if len(endedCO) == 1:
                endedCourses = '[' + generateCourseId() + ']'
            else:
                endedCourses = '[' + generateCourseId()
        elif x == endedCO[-1]:
            endedCourses = endedCourses + ',' + generateCourseId() + ']'
        else:
            endedCourses = endedCourses + ',' + generateCourseId()
    if endedCO == 0:
        endedCourses = '[]'
    return endedCourses

def generateSubPatternUnavailability (AARef):
    DateRef = AARef.split('-')
    inAAStart = date(int(DateRef[0]), 1, 1)
    inAAStop = date(int(DateRef[1]), 1, 1)
    dateStartToVerify = date
    dateStopToVerify = date
    startDate = ''
    stopDate = ''
    toReturn = ''
    startDatesControl = []
    stopDatesControl = []
    unavailDates = random.randrange(1, 10)
    for i in range(unavailDates):
        found = 1
        while found > 0:
            found = 0
            startDate = generateDate(1, DateRef)
            unavailDuration = random.randint(7, 14)
            stopDate = calculateSecondDate(startDate, unavailDuration)
            dateStartToVerify = date(int(startDate.split('-')[0]), int(startDate.split('-')[1]), int(startDate.split('-')[2]))
            dateStopToVerify = date(int(stopDate.split('-')[0]), int(stopDate.split('-')[1]), int(stopDate.split('-')[2]))
            value = int(stopDate.split('-')[0])
            for (start, stop) in zip(startDatesControl, stopDatesControl):
                if (start <= dateStartToVerify <= stop) or (start <= dateStopToVerify <= stop) or (inAAStart.year <= dateStopToVerify.year >= inAAStop.year):
                    found += 1
        startDatesControl.append(dateStartToVerify)
        stopDatesControl.append(dateStopToVerify)
        toReturn = toReturn + startDate + '|' + stopDate
        if i != range(unavailDates)[-1]:
            toReturn = toReturn + ';'
    return toReturn
