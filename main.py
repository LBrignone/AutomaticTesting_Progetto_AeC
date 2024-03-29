import random
from pathlib import Path
from datetime import date
from datetime import timedelta
from PatternGen import generatePattern
from SubPatternGen import *
from ElementGen import *
from DateDurationCalc import calculateSecondDate
from CONSTANTS import *

if __name__ == '__main__':
    patternToOut = ''
    fileNum = input("\ninserire la versione del file da generare: ")
    fileTypeGeneration = input("\ninserire il tipo di file da generare\n\t- p -> add persone\n\t- a -> add aule"
                               "\n\t- c -> add corsi\n\t- cs -> add corsi di studio\n\t- up -> update persone"
                               "\n\t- ua -> update aule\n\t- ic -> insert corso\n\t- pa -> indisponibilità professori"
                               "\n\t- s -> sessione d'esame\n\t- r -> corsi raggruppati\n--> ")
    if fileTypeGeneration != 'r' and fileTypeGeneration != 'pa':
        generate = input("inserire il numero di righe da generare: ")

    match fileTypeGeneration:
        case 'p':
            fileOfName = open(r"./FileToGenerateFrom/Nomi_PAEC.txt", 'r')
            fileOfSurname = open(r"./FileToGenerateFrom/Cognomi_PAEC.txt", 'r')
            fileOfMail = open(r"./FileToGenerateFrom/Mail_PAEC.txt", 'r')
            names = fileOfName.read()
            surnames = fileOfSurname.read()
            mails = fileOfMail.read()
            fileOfName.close()
            fileOfSurname.close()
            fileOfMail.close()
            listOfNames = names.split()
            listOfSurnames = surnames.split()
            listOfMails = mails.split()
            fileOutputP = open("automateGenPERSON_" + fileNum.rjust(2, '0') + ".txt", 'w')
            for i in range(int(generate, 10)):
                # person pattern generation
                name = random.choice(listOfNames)
                surname = random.choice(listOfSurnames)
                mail = name + '.' + surname + '@' + random.choice(listOfMails)
                patternToOut = generatePattern(name, surname, mail)
                fileOutputP.write(patternToOut)
                if i != int(generate, 10):
                    fileOutputP.write('\n')
            fileOutputP.close()

        case 'a':
            ClList = []
            fileOutputCl = open("automateGenCLASSROOM_" + fileNum.rjust(2, '0') + ".txt", 'w')

            for i in range(int(generate, 10)):
                status = 0
                # classroom pattern generation
                while status == 0:
                    status = 1
                    ClGen = generateRoom(1)
                    for element in ClList:
                        if element == ClGen:
                            status = 0
                    if status == 1:
                        ClList.append(ClGen)
                        maxCap = random.randint(MIN_CLASSROOM_CAP, MAX_CLASSROOM_CAP)
                        patternToOut = generatePattern(random.choice(['A', 'L']), ClGen, str(maxCap), str(random.randint(20, maxCap)))
                fileOutputCl.write(patternToOut)
                if i != int(generate, 10):
                    fileOutputCl.write('\n')
            fileOutputCl.close()

        case 'c':
            id = []
            fileOfCourse = open(r"./FileToGenerateFrom/Corsi_PAEC.txt", 'r')
            courses = fileOfCourse.read()
            fileOfCourse.close()
            try:
                with open(r"../../CLionProjects/Progetto/cmake-build-debug/db_professori.txt") as fileOfProfIds:
                    for line in fileOfProfIds:
                        id.append(line.split(';')[0])
            except IOError:
                print("\nfile di database per i professori non trovato generazione \"automatica\" degli id dei professori nei corsi")
                numProf = input("\ninserire il numero di professori da generare: ")
                for j in range(int(numProf, 10)):
                    id.append(generateProfId(0, j))
            listOfCourses = courses.split('\n')
            fileOutputCo = open("automateGenCOURSE_" + fileNum.rjust(2, '0') + ".txt", 'w')

            cycleNum = int(generate, 10)
            for i in range(cycleNum):
                lessonH = random.randint(MIN_HOUR, MAX_HOUR)
                exerciH = random.randint(MIN_HOUR, MAX_HOUR)
                laboraH = random.randint(MIN_HOUR, MAX_HOUR)
                numOfVer = random.randint(MIN_VERSION_NUM, MAX_VERSION_NUM)
                numOfVerList = range(numOfVer)
                courseNameChoose = random.choice(listOfCourses)
                listOfCourses.remove(courseNameChoose)
                patternToOut = generatePattern(generateDate(0,''), courseNameChoose,str(random.randint(MIN_CFU, MAX_CFU)),
                                               str(lessonH), str(exerciH), str(laboraH), 'attivo', numOfVer,
                                               generateSubPatternProfOrg(id, lessonH, exerciH, laboraH, numOfVerList, 0),
                                               generateSubPatternExamOrg(), generateSubPatternGroupedCourses(cycleNum, i))
                fileOutputCo.write(patternToOut)
                if i != int(generate, 10):
                    fileOutputCo.write('\n')
            fileOutputCo.close()

        case 'cs':
            # course of study pattern generation
            courses = ''
            session = ''
            id = []

            fileOutputCoS = open("automateGenCOURSEofSTUDY_" + fileNum.rjust(2, '0') + ".txt", 'w')
            try:
                with open(r"../../CLionProjects/Progetto/cmake-build-debug/db_corsi.txt") as fileOfCourseIds:
                    for line in fileOfCourseIds:
                        if line.split(';')[0] == 'c':
                            id.append(line.split(';')[1])
            except IOError:
                print("\nfile di database per i professori non trovato\ngenerazione \"automatica\" degli id dei professori nei corsi")
                id.append(generateCourseIdList(int(generate, 10)))

            for i in range(int(generate, 10)):
                copyCourseIds = []
                copyCourseIds.clear()
                copyCourseIds.append(id[0 : len(id) // 2].copy())
                copyCourseIds.append(id[(len(id) // 2) + 1 : -1].copy())
                bs_ms = random.choice([SEMESTER_NUM_BS, SEMESTER_NUM_MS])
                bs_ms_List = range(bs_ms)
                for n in bs_ms_List:
                    courseNum = range(random.randint(MIN_COURSE_OF_STUDY, MAX_COURSE_OF_STUDY))
                    for m in courseNum:
                        choseCourseIds = random.choice(copyCourseIds[n % 2])
                        copyCourseIds[n % 2].remove(choseCourseIds)
                        if m == 0:
                            if len(courseNum) == 1:
                                courses = '{' + choseCourseIds + '}'
                            else:
                                courses = '{' + choseCourseIds
                        elif m == courseNum[-1]:
                            courses = courses + ',' + choseCourseIds + '}'
                        else:
                            courses = courses + ',' + choseCourseIds
                    if n == 0:
                        session = '[' + courses
                    elif n == bs_ms_List[-1]:
                        session = session + ',' + courses + ']'
                    else:
                        session = session + ',' + courses
                if bs_ms == 6:
                    degree = 'BS'
                else:
                    degree = 'MS'
                patternToOut = generatePattern(degree, session)
                fileOutputCoS.write(patternToOut)
                if i != int(generate, 10):
                    fileOutputCoS.write('\n')
            fileOutputCoS.close()

        case 'up':
            # person update generation
            studentId = []
            professorId = []
            fileOfName = open(r"./FileToGenerateFrom/Nomi_PAEC.txt", 'r')
            names = fileOfName.read()
            fileOfName.close()
            listOfNames = names.split()
            fileOfSurname = open(r"./FileToGenerateFrom/Cognomi_PAEC.txt", 'r')
            surnames = fileOfSurname.read()
            fileOfSurname.close()
            listOfSurnames = surnames.split()
            fileOfMail = open(r"./FileToGenerateFrom/Mail_PAEC.txt", 'r')
            mails = fileOfMail.read()
            fileOfMail.close()
            listOfMails = mails.split()
            fileOfStudents = open(r"../../CLionProjects/Progetto/cmake-build-debug/db_studenti.txt", 'r')
            completeStudentFile = fileOfStudents.read()
            fileOfStudents.close()
            completeStudent = completeStudentFile.split('\n')
            for i in completeStudent:
                studentElements = i.split(';')
                studentId.append(studentElements[0])
            fileOfProfessors = open(r"../../CLionProjects/Progetto/cmake-build-debug/db_professori.txt", 'r')
            completeProfessorFile = fileOfProfessors.read()
            fileOfProfessors.close()
            completeProfessor = completeProfessorFile.split('\n')
            for i in completeProfessor:
                professorElements = i.split(';')
                professorId.append(professorElements[0])
            fileOutputUPS = open("automateGenUPDATESTUDENTS_" + fileNum.rjust(2, '0') + ".txt", 'w')
            fileOutputUPD = open("automateGenUPDATEPROFESSOR_" + fileNum.rjust(2, '0') + ".txt", 'w')

            for i in range(int(generate, 10)):
                name = random.choice(listOfNames)
                surname = random.choice(listOfSurnames)
                mail = name + '.' + surname + '@' + random.choice(listOfMails)
                studentToModify = random.choice(studentId)
                professorToModify = random.choice(professorId)
                nameChoice = random.choice(['', name])
                surnameChoice = random.choice(['', surname])
                mailChoice = random.choice(['', mail])
                patternToOut = generatePattern(studentToModify, nameChoice, surnameChoice, mailChoice)
                fileOutputUPS.write(patternToOut)
                patternToOut = generatePattern(professorToModify, nameChoice, surnameChoice, mailChoice)
                fileOutputUPD.write(patternToOut)
                if i != int(generate, 10):
                    fileOutputUPS.write('\n')
                    fileOutputUPD.write('\n')
            fileOutputUPS.close()
            fileOutputUPD.close()

        case 'ua':
            # classroom update generation
            classroomId = []
            capacity = []
            examCapacity = []
            with  open(r"../../CLionProjects/Progetto/cmake-build-debug/db_aule.txt", 'r') as fileOfClassroom:
                for line in fileOfClassroom:
                    classroomElement = line.split(';')
                    classroomId.append(classroomElement[0])
                    capacity.append(classroomElement[3])
                    examCapacity.append(classroomElement[4])
            fileOutputUCl = open("automateGenUPDATECLASSROOM_" + fileNum.rjust(2, '0') + ".txt", 'w')

            for i in range(int(generate, 10)):
                ClGen = generateRoom(1)
                classroomTyChoice = random.choice(['A', 'L', ''])
                classroomToModify = random.choice(classroomId)
                maxCap = random.randint(MIN_CLASSROOM_CAP, MAX_CLASSROOM_CAP)
                nameChoice = random.choice(['', ClGen])
                capChoice = random.choice(['', maxCap])
                examCapChoice = random.choice(['', random.randint(MIN_CLASSROOM_CAP, maxCap)])
                patternToOut = generatePattern(classroomToModify, classroomTyChoice, ClGen, str(capChoice), str(examCapChoice))
                fileOutputUCl.write(patternToOut)
                if i != int(generate, 10):
                    fileOutputUCl.write('\n')
            fileOutputUCl.close()

        case 'ic':
            # course insert generator
            courseId = []
            professorId = []
            lessonH = []
            exerciH = []
            laboraH = []
            professorForVersion = []    # here are registered the number of professors for a given version of a course -> [a, b, c]
            professorForCourse = []     # here are registered the number of professors for a given course -> [[a, b, c], [d, e, f], ...]
            counter = 0
            try:
                with open(r"../../CLionProjects/Progetto/cmake-build-debug/db_corsi.txt") as fileOfCourses:
                    for line in fileOfCourses:
                        if line.startswith('c'):
                            courseElement = line.split(';')
                            courseId.append(courseElement[1])
                            lessonH.append(courseElement[-3])
                            exerciH.append(courseElement[-2])
                            laboraH.append(courseElement[-1])
                        if line.startswith('a'):
                            courseElement = line.split('{')
                            courseElement.pop(0)
                            for j in courseElement:
                                version = j.split(',')
                                if version[0].startswith('d'):
                                    counter += 1
                                else:
                                    professorForVersion.append(counter)
                                    counter = 0
                            professorForVersion.pop(0)
                            professorForCourse.append(professorForVersion)
            except IOError:
                print("\nfile di database per i corsi non trovato generazione \"automatica\" degli id dei corsi")
                numProf = input("\ninserire il numero di professori da generare: ")
                for j in range(int(numProf, 10)):
                    professorId.append(generateProfId(0, j))
            try:
                with open(r"../../CLionProjects/Progetto/cmake-build-debug/db_professori.txt") as fileOfProfIds:
                    for line in fileOfProfIds:
                        professorId.append(line.split(';')[0])
            except IOError:
                print("\nfile di database per i professori non trovato generazione \"automatica\" degli id dei professori nei corsi")
                numProf = input("\ninserire il numero di professori da generare: ")
                for j in range(int(numProf, 10)):
                    professorId.append(generateProfId(0, j))
            fileOutputUCo = open("automateGenINSERTCOURSE_" + fileNum.rjust(2, '0') + ".txt", 'w')

            cycleNum = int(generate, 10)
            for i in range(cycleNum):
                dateChoice = generateDate(0, MIN_ACADEMIC_YEAR, MAX_ACADEMIC_YEAR)
                courseStatusUpdate = random.choice(['attivo', 'non_attivo', ''])
                versionUpdateNum = random.randint(1, 4)
                versionUpdateNumList = range(versionUpdateNum)
                courseToModify = random.choice(courseId)
                numProfPerVer = professorForCourse[courseId.index(courseToModify)]
                lessonHUP = int(lessonH[courseId.index(courseToModify)])
                exerciHUP = int(exerciH[courseId.index(courseToModify)])
                laboraHUP = int(laboraH[courseId.index(courseToModify)])
                inheritPRoOrg = random.choice(['', generateSubPatternProfOrg(professorId, lessonHUP, exerciHUP, laboraHUP, versionUpdateNumList, 0, numProfPerVer)])
                examOrgChoice = random.choice(['', generateSubPatternExamOrg()])
                groupedChoice = random.choice(['', generateSubPatternGroupedCourses(cycleNum, i)])
                patternToOut = generatePattern(courseToModify, dateChoice, courseStatusUpdate, versionUpdateNum, inheritPRoOrg, examOrgChoice, groupedChoice)
                fileOutputUCo.write(patternToOut)
                if i != int(generate, 10):
                    fileOutputUCo.write('\n')
            fileOutputUCo.close()

        case 'pa':
            # indisponibilità professori
            professorUnavail = ''
            professorAlreadyChoose = ['']
            professorId = []
            academicYear = input("inserire l'anno accademico di riferimento (formato AAAA-AAAA): ")
            try:
                with open(r"../../CLionProjects/Progetto/cmake-build-debug/db_professori.txt") as fileOfProfIds:
                    for line in fileOfProfIds:
                        professorId.append(line.split(';')[0])
            except IOError:
                print("\nfile di database per i professori non trovato generazione \"automatica\" degli id dei professori nei corsi")
                numProf = input("\ninserire il numero di professori da generare: ")
                for j in range(int(numProf, 10)):
                    professorId.append(generateProfId(0, j))
            fileOutputUnv = open("automateGenUNAVAILABILITY_" + academicYear + "_" + fileNum.rjust(2, '0') + ".txt", 'w')
            for i in range(len(professorId)):
                if len(professorAlreadyChoose) < len(professorId):
                    while professorUnavail in professorAlreadyChoose:
                        professorUnavail = random.choice(professorId)
                    professorAlreadyChoose.append(professorUnavail)
                    patternToOut = generatePattern(professorUnavail, generateSubPatternUnavailability(academicYear)) #generatePattern(generateProfId(1, 0, 1))
                    fileOutputUnv.write(patternToOut)
                    if i != len(professorId):
                        fileOutputUnv.write('\n')
                else:
                    print("error: non abbastanza professori")
                    break
            fileOutputUnv.close()

        case 's':
            i = 0
            position1 = 0
            position2 = 0
            prev = 0
            singleDate = ''
            academicYear = ''
            dateValStart = []
            dateValStop = []
            fileOutputS = open("automateGenEXAMSESSION_" + fileNum.rjust(2, '0') + ".txt", 'w')
            while i < int(generate, 10):
                index = 0
                academicYear = generateDate(0,)
                academicYearSplitted = academicYear.split('-')
                for j in range(3):
                    singleDate = generateDate(1, academicYearSplitted)
                    tmp = date.fromisoformat(singleDate)
                    dateValStart.append(tmp)
                    if index == 0 or index == 1:
                        dateValStop.append(dateValStart[index] + timedelta(days=SESSION_1_AND_2_DURATION))
                    else:
                        dateValStop.append(dateValStart[index] + timedelta(days=SESSION_3_DURATION))
                    index += 1
                if (dateValStart[0] < dateValStart[1] < dateValStart[2]) and (dateValStop[0] < dateValStop[1] < dateValStop[2]):
                    for (k, l) in zip(dateValStart, dateValStop):
                        position1 += 1
                        for (m, n) in zip(dateValStart, dateValStop):
                            position2 += 1
                            if k <= m <= l or k <= n <= l:
                                if position1 != position2:
                                    dateValStart.clear()
                                    dateValStop.clear()
                                    i -= 1
                            elif (m.year != int(academicYearSplitted[0]) and m.year != int(academicYearSplitted[1])) or (n.year != int(academicYearSplitted[0]) and n.year != int(academicYearSplitted[1])):
                                dateValStart.clear()
                                dateValStop.clear()
                                i -= 1
                        position2 = 0
                    position1 = 0
                else:
                    dateValStart.clear()
                    dateValStop.clear()
                    i -= 1
                i += 1
                if i > prev:
                    prev = i
                    fileOutputS.write("-s current_a " + academicYear)
                    for (o, p) in zip(dateValStart, dateValStop):
                        fileOutputS.write(" " + o.isoformat() + "_" + p.isoformat())
                    if i < int(generate, 10):
                        fileOutputS.write("\n")
            fileOutputS.close()

        case 'r':
            firstSemester = []
            secondSemester = []
            tmpSemester = []
            val = 0
            courseId = ''
            fileOutputGrouped = open("automateGenGROUPEDCOURSES_" + fileNum.rjust(2, '0') + ".txt", 'w')
            with open(r"../../CLionProjects/Progetto/cmake-build-debug/db_corsi_studio.txt", 'r') as fileOfCourseOfStudy:
                for line in fileOfCourseOfStudy:
                    firstSeparation = line.split(';')
                    coursesBySemester = firstSeparation[2].split('{')
                    coursesBySemester.pop(0)
                    for courses in coursesBySemester:
                        course = courses.split(',')
                        for verification in course:
                            if verification:
                                if verification.endswith('}]\n'):
                                    verification = verification[0:-3]
                                    if val == 0:
                                        firstSemester.append(verification)
                                    else:
                                        secondSemester.append(verification)
                                elif verification.endswith('}]'):
                                    verification = verification[0:-2]
                                    if val == 0:
                                        firstSemester.append(verification)
                                    else:
                                        secondSemester.append(verification)
                                elif verification.endswith('}'):
                                    verification = verification[0:-1]
                                    if val == 0:
                                        firstSemester.append(verification)
                                    else:
                                        secondSemester.append(verification)
                                    if val == 0:
                                        val += 1
                                    else:
                                        val -= 1
                                else:
                                    if val == 0:
                                        firstSemester.append(verification)
                                    else:
                                        secondSemester.append(verification)
            with open(r'../../CLionProjects/Progetto/cmake-build-debug/db_corsi.txt', 'r') as fileOfCourses:
                for course in fileOfCourses:
                    choice = ''
                    if course.startswith('c'):
                        tmpSemester.clear()
                        tmp = course.split(';')
                        courseId = tmp[1]
                        fileOutputGrouped.write(course)
                        if firstSemester.count(courseId) > 0:
                            tmpSemester = firstSemester.copy()
                            tmpSemester.remove(courseId)
                        elif secondSemester.count(courseId) > 0:
                            tmpSemester = secondSemester.copy()
                            tmpSemester.remove(courseId)
                    else:
                        tmp = course.split(';')
                        tmp = generatePattern(tmp[0], tmp[1], tmp[2], tmp[3], tmp[4], tmp[5])
                        if len(tmpSemester) > 0:
                            num = range(random.randint(0, 4))
                            for grouped in num:
                                choice += random.choice(tmpSemester)
                                if grouped != num[-1]:
                                    choice += ','
                        else:
                            num = 0
                        tmp += ';{' + choice + '}\n'
                        fileOutputGrouped.write(tmp)
            p = Path(r"../../CLionProjects/Progetto/cmake-build-debug/db_corsi.txt")
            p.unlink()
            Path(r"./automateGenGROUPEDCOURSES_" + fileNum.rjust(2, '0') + ".txt").replace(p)
