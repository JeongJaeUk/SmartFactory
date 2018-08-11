def getAvailableList(matrix, item):
    numlist = []
    for i in matrix:
        if item in i:
            numlist.append(i[0])

    return numlist

def getWorkingTime(matrix, item):
    for i in matrix:
        if item in i:
            time = i[1]

    return time