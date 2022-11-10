import string

def generatePattern (*elements):
    pattern = ''
    i = 1
    for val in elements:
        pattern = pattern + str(val)
        if i != len(elements):
            pattern = pattern + ';'
        i += 1
    return pattern
