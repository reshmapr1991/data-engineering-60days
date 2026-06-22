

def getRemovableIndices(str1, str2):

    result = []

    for i in range(len(str1)):
        new_str = str1[:i] + str1[i + 1:]

        if new_str == str2:
            result.append(i)

    return (result)

str1 = "abdgggda"
str2 = "abdggda"
print(getRemovableIndices(str1, str2))
