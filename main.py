import random
from datetime import date
from datetime import timedelta
from PatternGen import generatePattern
from SubPatternGen import generateSubPatternProfOrg
from SubPatternGen import generateSubPatternExamOrg
from SubPatternGen import generateSubPatternGroupedCourses
from SubPatternGen import generateSubPatternUnavailability
from ElementGen import generateRoom
from ElementGen import generateDate
from ElementGen import generateProfId
from ElementGen import generateCourseId
from DateDurationCalc import calculateSecondDate

if __name__ == '__main__':
    patternToOut = ''
    generate = input("inserire il numero di righe da generare: ")
    fileNum = input("\ninserire una versione del file da generare: ")
    fileTypeGeneration = input("\ninserire il tipo di file da generare\n\t- p -> add persone\n\t- a -> add aule"
                               "\n\t- c -> add corsi\n\t- cs -> add corsi di studio\n\t- up -> update persone"
                               "\n\t- ua -> update aule\n\t- ic -> insert course\n\t- sa -> set availability"
                               "\n\t- s -> exam session\n--> ")

    match fileTypeGeneration:
        case 'p':
            fileOfName = open(r"../../Desktop/Nomi_PAEC.txt", 'r')
            fileOfSurname = open(r"../../Desktop/Cognomi_PAEC.txt", 'r')
            fileOfMail = open(r"../../Desktop/Mail_PAEC.txt", 'r')
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
                        maxCap = random.randint(20, 400)
                        patternToOut = generatePattern(random.choice(['A', 'L']), ClGen, str(maxCap), str(random.randint(20, maxCap)))
                fileOutputCl.write(patternToOut)
                if i != int(generate, 10):
                    fileOutputCl.write('\n')
            fileOutputCl.close()

        case 'c':
            fileOfCourse = open(r"../../Desktop/Corsi_PAEC.txt", 'r')
            courses = fileOfCourse.read()
            fileOfCourse.close()
            listOfCourses = courses.split('\n')
            fileOutputCo = open("automateGenCOURSE_" + fileNum.rjust(2, '0') + ".txt", 'w')

            for i in range(int(generate, 10)):
                lessonH = random.randint(1, 100)
                exerciH = random.randint(1, 100)
                laboraH = random.randint(1, 100)
                numOfVer = random.randint(1, 4)
                numOfVerList = range(numOfVer)
                patternToOut = generatePattern(generateDate(0), random.choice(listOfCourses),
                                               str(random.randint(6, 10)), str(lessonH), str(exerciH), str(laboraH), 'attivo',
                                               numOfVer,
                                               generateSubPatternProfOrg(generateProfId(1, 0, 1), lessonH, exerciH, laboraH, numOfVerList, 0),
                                               generateSubPatternExamOrg(1), generateSubPatternGroupedCourses())
                fileOutputCo.write(patternToOut)
                if i != int(generate, 10):
                    fileOutputCo.write('\n')
            fileOutputCo.close()

        case 'cs':
            # course of study pattern generation
            courses = ''
            session = ''

            fileOutputCoS = open("automateGenCOURSEofSTUDY_" + fileNum.rjust(2, '0') + ".txt", 'w')
            for i in range(int(generate, 10)):
                bs_ms = random.choice([6, 4])
                bs_ms_List = range(bs_ms)
                for n in bs_ms_List:
                    courseNum = range(random.randint(1, 4))
                    for m in courseNum:
                        if m == 0:
                            if len(courseNum) == 1:
                                courses = '{' + generateCourseId() + '}'
                            else:
                                courses = '{' + generateCourseId()
                        elif m == courseNum[-1]:
                            courses = courses + ',' + generateCourseId() + '}'
                        else:
                            courses = courses + ',' + generateCourseId()
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
            fileOfName = open(r"../../Desktop/Nomi_PAEC.txt", 'r')
            names = fileOfName.read()
            fileOfName.close()
            listOfNames = names.split()
            fileOfSurname = open(r"../../Desktop/Cognomi_PAEC.txt", 'r')
            surnames = fileOfSurname.read()
            fileOfSurname.close()
            listOfSurnames = surnames.split()
            fileOfMail = open(r"../../Desktop/Mail_PAEC.txt", 'r')
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
            fileOutputUPD = open("automateGenUPDATEPROFESSOR" + fileNum.rjust(2, '0') + ".txt", 'w')

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
            fileOfClassroom = open(r"../../CLionProjects/Progetto/cmake-build-debug/db_aule.txt", 'r')
            completeClassroomFile = fileOfClassroom.read()
            fileOfClassroom.close()
            completeClassroom = completeClassroomFile.split('\n')
            for i in completeClassroom:
                classroomElement = i.split(';')
                classroomId.append(classroomElement[0])
            fileOutputUCl = open("automateGenUPDATECLASSROOM_" + fileNum.rjust(2, '0') + ".txt", 'w')

            for i in range(int(generate, 10)):
                ClGen = generateRoom(1)
                maxCap = random.randint(20, 400)
                classroomTyChoice = random.choice(['A', 'L', ''])
                classroomToModify = random.choice(classroomId)
                nameChoice = random.choice(['', ClGen])
                capChoice = random.choice(['', maxCap])
                examCapChoice = random.choice(['', random.randint(20, maxCap)])
                patternToOut = generatePattern(classroomToModify, classroomTyChoice, ClGen, str(capChoice), str(examCapChoice))
                fileOutputUCl.write(patternToOut)
                if i != int(generate, 10):
                    fileOutputUCl.write('\n')
            fileOutputUCl.close()

        case 'ic':
            # course insert generator
            courseId = []
            fileOfCourses = open(r"../../CLionProjects/Progetto/cmake-build-debug/db_corsi.txt")
            completeCourseFile = fileOfCourses.read()
            fileOfCourses.close()
            completeCourse = completeCourseFile.split()
            for i in completeCourseFile:
                if i.startswith('c'):
                    courseElement = i.split(';')
                    courseId.append(courseElement[0])
            fileOutputUCo = open("automateGenUPDATECOURSE_" + fileNum.rjust(2, '0') + ".txt", 'w')

            for i in range(int(generate, 10)):
                dateChoice = generateDate(0)
                courseStatusUpdate = random.choice(['attivo', 'non_attivo', ''])
                versionUpdateNum = random.randint(1, 4)
                versionUpdateNumList = range(versionUpdateNum)
                lessonHUP = random.randint(1, 100)
                exerciHUP = random.randint(1, 100)
                laboraHUP = random.randint(1, 100)
                courseToModify = random.choice(courseId)
                inheritPRoOrg = random.choice(['', generateSubPatternProfOrg(generateProfId(1, 0, 1), lessonHUP, exerciHUP, laboraHUP, versionUpdateNumList, 1)])
                examOrgChoice = random.choice(['', generateSubPatternExamOrg(1)])
                groupedChoice = random.choice(['', generateSubPatternGroupedCourses()])
                patternToOut = generatePattern(courseToModify, dateChoice, courseStatusUpdate, versionUpdateNum, inheritPRoOrg, examOrgChoice, groupedChoice)
                fileOutputUCo.write(patternToOut)
                if i != int(generate, 10):
                    fileOutputUCo.write('\n')
            fileOutputUCo.close()

        case 'sa':
            professorUnavail = ''
            professorAlreadyChoose = ['']
            professorId = []
            academicYear = input("inserire l'anno accademico di riferimento (formato AAAA-AAAA): ")
            fileOfProfessors = open(r"../../CLionProjects/Progetto/cmake-build-debug/db_professori.txt", 'r')
            completeProfessorFile = fileOfProfessors.read()
            fileOfProfessors.close()
            completeProfessor = completeProfessorFile.split('\n')
            for i in completeProfessor:
                professorElements = i.split(';')
                professorId.append(professorElements[0])
            fileOutputUnv = open("automateGenUNAVAILABILITY_" + academicYear + "_" + fileNum.rjust(2, '0') + ".txt", 'w')
            for i in range(int(generate, 10)):
                while professorUnavail in professorAlreadyChoose:
                    professorUnavail = random.choice(professorId)
                professorAlreadyChoose.append(professorUnavail)
                patternToOut = generatePattern(professorUnavail, generateSubPatternUnavailability(academicYear)) #generatePattern(generateProfId(1, 0, 1))
                fileOutputUnv.write(patternToOut)
                if i != int(generate, 10):
                    fileOutputUnv.write('\n')
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
                academicYear = generateDate(0,'nul')
                academicYearSplitted = academicYear.split('-')
                for j in range(3):
                    singleDate = generateDate(0, academicYearSplitted)
                    tmp = date.fromisoformat(singleDate)
                    dateValStart.append(tmp)
                    if index == 0 or index == 1:
                        dateValStop.append(dateValStart[index] + timedelta(days=42))
                    else:
                        dateValStop.append(dateValStart[index] + timedelta(days=28))
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