import os
import math
import random
from fileinput import close



DEFAULT_COMMENT = "#"



def isEndOfFile(file):
    return (file.tell() == os.fstat(file.fileno()).st_size)


def countNbrLine(fileName):
    return sum(1 for line in open(fileName))


def nextMeaningLine(file, commentString=DEFAULT_COMMENT):
    while (not isEndOfFile(file)):
        res = file.readline().strip()
        if (res.startswith(commentString)):
            continue
        elif (res == "\n" or res == ""):
            continue
        else:
            return res
    raise Exception("No useful string found in the file " + file.name)


def swapFileLines(sampleProportion, allFileName, pathInputFile, pathOutputFile1, pathOutputFile2):
    if (sampleProportion < .0 or sampleProportion > 1.):
        raise Exception("Wrong proportion value: " + learningSampleProportion)

    nbrLineInput    = countNbrLine(pathInputFile    + allFileName)
    fileInput       = open(pathInputFile    + allFileName, 'r')
    fileOutput1     = open(pathOutputFile1  + allFileName, 'w')
    fileOutput2     = open(pathOutputFile2  + allFileName, 'w')
    nbrLintOutput1  = int(nbrLineInput * sampleProportion)
    nbrLintOutput2  = nbrLineInput - nbrLintOutput1

    for i in xrange(nbrLineInput):
        line    = nextMeaningLine(fileInput)
        if (nbrLintOutput1 > nbrLintOutput2):
            newProportion = .5 - float(nbrLintOutput2) / float(nbrLintOutput1)
        else:
            newProportion = .5 + float(nbrLintOutput1) / float(nbrLintOutput2)

        rnd     = random.uniform(.0, newProportion)
        if (rnd <= sampleProportion):
            fileOutput1.write(line + "\n")
            nbrLintOutput1 -= 1
        else:
            fileOutput2.write(line + "\n")
            nbrLintOutput2 -= 1

    fileInput   .close()
    fileOutput1 .close()
    fileOutput2 .close()


def normalizeSample(sample):
    maxElement  = None
    sampleParsed= []
    for x in sample[0:]:
        try:
            xParsed = float(x)
        except ValueError:
            if len(x) == 1:
                xParsed = ord(x)
            else:
                raise Exception("Can not normalize a sample containing the value: " + x)
        sampleParsed.append(xParsed)
        if (maxElement == None or maxElement < xParsed):
            maxElement = xParsed

    result = [sample[0]]
    for xParsed in sampleParsed:
        result.append(xParsed / maxElement)

    return result


def roughlyProportional(proportion, value0, value1, gap=100):
    prod = value0 * proportion
    if ((prod < value1 - gap) or (prod > value1 + gap)):
        print "\t\t\t* Proportion = " + str(proportion) + "    value0 = " + str(value0) + "    value1 = " + str(value1)
        return False
    return True

