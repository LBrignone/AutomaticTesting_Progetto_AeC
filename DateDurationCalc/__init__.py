def calculateSecondDate (date, duration):
    inRange = 0
    day = int(date.split('-')[2])
    month = int(date.split('-')[1])
    year = int(date.split('-')[0])

    day += duration
    while inRange == 0:
        if month == 4 or month == 6 or month == 9 or month == 11:
            if day > 30:
                month += 1
                day -= 30
            else:
                inRange = 1
        elif month == 2:
            if day > 28:
                month += 1
                day -= 28
            else:
                inRange = 1
        else:
            if day > 31:
                if month == 12:
                    year += 1
                    month = 1
                else:
                    month += 1
                day -= 31
            else:
                inRange = 1
    date = str(year) + '-' + str(month).rjust(2, '0') + '-' + str(day).rjust(2, '0')
    return date

