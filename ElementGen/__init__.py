import random
import string

def generateRoom (insertError):
    if insertError == 0:
        id = 'A' + str(random.randrange(1, 20)).rjust(3, '0')
    else:
        roomTy = ['Aula', 'Led', 'Laib']
        roomFloor = ['S', 'I', 'A', 'B', 'C', 'D', 'P', 'R']

        id = random.choice(roomTy) + ' ' + str(random.randrange(1, 20)) + random.choice(roomFloor)
    return id

def generateDate (isAA, *AAref):
    if AAref[0] == 'nul':
        if isAA == 0:
            year = random.randint(2000, 2022)
            date = str(year) + '-' + str(year + 1)
        else:
            year = random.randint(2000, 2022)
            month = random.randint(1, 12)
            if month == 4 or month == 6 or month == 9 or month == 11:
                day = random.randint(1, 30)
            elif month == 2:
                day = random.randint(1, 28)
            else:
                day = random.randint(1, 31)
            date = str(year) + '-' + str(month).rjust(2, '0') + '-' + str(day).rjust(2, '0')
    else:
        year = random.choice(AAref[0])
        month = random.randint(1, 12)
        if month == 4 or month == 6 or month == 9 or month == 11:
            day = random.randint(1, 30)
        elif month == 2:
            day = random.randint(1, 28)
        else:
            day = random.randint(1, 31)
        date = str(year) + '-' + str(month).rjust(2, '0') + '-' + str(day).rjust(2, '0')
    return date

def generateProfId(consec, prev, insertError):
    if insertError == 0:
        if consec == 0:
            tmp = int(prev)
            tmp += 1
            numId = str(tmp)
            numId.rjust(6, '0')
            numId = 'd' + numId
        else:
            numId = str(random.randint(0, 999999))
            numId.rjust(6, '0')
            numId = 'd' + numId
    else:
        if consec == 0:
            tmp = int(prev)
            tmp += 1
            numId = 'd' + str(tmp).rjust(6, '0')
        else:
            tmp = random.randint(0, 999999)
            numId = 'd' + str(tmp).rjust(6, '0')
    return numId

def generateVersion (prev, insertError):
    if insertError == 0:
        verId = prev + 1
        verId = 'P' + str(verId).rjust(3, '0')
    else:
        verId = random.choice(string.ascii_uppercase) + str(random.randint(1, 999)).rjust(3, '0')
    return verId

def generateCourseId():
    letId = ''
    for i in range(5):
        letId = letId + random.choice(string.ascii_uppercase)
    numId = '01' + letId
    return numId