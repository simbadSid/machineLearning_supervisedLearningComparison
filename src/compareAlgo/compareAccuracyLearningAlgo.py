from ProblemInstance import ProblemInstance
from util import *
import sys
import os
import numpy as np
import matplotlib.pyplot as plt




PARAMETER_TEST_SAMPLE          = "testSample"
PARAMETER_CLEAN_SAMPLE         = "clean"
PARAMETER_NORMALIZED_DATA       = "normalized"

PATH_LEARNING_ALGO             = "../learningAlgo/"

PATH_TEST_SET                  = "../../resource/sample/sampleRow/"
PATH_TEST_SET_NORMALIZED       = "../../resource/sample/sampleRowNormalized/"

PATH_SAMPLE_LEARN              = "../../resource/sample/sampleLearn/"
PATH_SAMPLE_LEARN_NORMALIZED   = "../../resource/sample/sampleLearnNormalized/"

PATH_SAMPLE_TEST               = "../../resource/sample/sampleTest/"
PATH_SAMPLE_TEST_NORMALIZED    = "../../resource/sample/sampleTestNormalized/"

PATH_PARAMETER                 = "../../resource/outputParameter/"
PATH_PROGRAM                   = "../"
PATH_PROGRAM_OUTPUT            = "../../resource/outputProgram/"
LEARNING_SAMPLE_PROPORTION     = .6





def cleanSample():
    pathDirList = [PATH_SAMPLE_LEARN, PATH_SAMPLE_TEST, PATH_TEST_SET_NORMALIZED, PATH_SAMPLE_LEARN_NORMALIZED, PATH_SAMPLE_TEST_NORMALIZED, PATH_PARAMETER, PATH_PROGRAM_OUTPUT]

    for path in pathDirList:
        for file in os.listdir(path):
            os.unlink(path + file)


def testSample():
    errorList = []
    for fileName in os.listdir(PATH_TEST_SET):
        nbrLineRowFile        = countNbrLine(PATH_TEST_SET + fileName)
        nbrLineRowFileNormal  = countNbrLine(PATH_TEST_SET_NORMALIZED + fileName)
        if (nbrLineRowFile != nbrLineRowFileNormal):
            errorList.append("Wrong number of lines in normalized sample file: " + fileName)

        nbrLineLearn        = countNbrLine(PATH_SAMPLE_LEARN            + fileName)
        nbrLineLearnNormal  = countNbrLine(PATH_SAMPLE_LEARN_NORMALIZED + fileName)
        nbrLineTest         = countNbrLine(PATH_SAMPLE_TEST             + fileName)
        nbrLineTestNormal   = countNbrLine(PATH_SAMPLE_TEST_NORMALIZED  + fileName)

        if (False == roughlyProportional(LEARNING_SAMPLE_PROPORTION, nbrLineRowFile, nbrLineLearn)):
            errorList.append("The sample learn file \"" + fileName + "\" does not respect the proportion " + str(LEARNING_SAMPLE_PROPORTION))
        if (False == roughlyProportional(LEARNING_SAMPLE_PROPORTION, nbrLineRowFile, nbrLineLearnNormal)):
            errorList.append("The normalized sample learn file \"" + fileName + "\" does not respect the proportion " + str(LEARNING_SAMPLE_PROPORTION))
        if (False == roughlyProportional(1-LEARNING_SAMPLE_PROPORTION, nbrLineRowFile, nbrLineTest)):
            errorList.append("The sample test file \"" + fileName + "\" does not respect the proportion " + str(LEARNING_SAMPLE_PROPORTION))
        if (False == roughlyProportional(1-LEARNING_SAMPLE_PROPORTION, nbrLineRowFile, nbrLineTestNormal)):
            errorList.append("The normalized sample test file \"" + fileName + "\" does not respect the proportion " + str(LEARNING_SAMPLE_PROPORTION))

    print "------------------------------------------------"
    print
    if (len(errorList) == 0):
        print "\t All samples have been successfully tested"
    else:
        for msg in errorList:
            print "\t -) " + msg
    print
    print "------------------------------------------------"




def plotBarComparison(nbrTest, isNormalizedData, learnErrorMinList, learnErrorMaxList, learnErrorAvgList, testErrorMinList, testErrorMaxList, testErrorAvgList, algoNameList):
    fig, ax = plt.subplots()
    index   = np.arange(nbrTest)
    barWidth= .35

    learnDistMin    = [learnErrorAvgList[i] - learnErrorMinList[i] for i in xrange(len(learnErrorAvgList))]
    testDistMin     = [testErrorAvgList[i]  - testErrorMinList[i]  for i in xrange(len(testErrorAvgList))]
    learnDistMax    = [learnErrorMaxList[i] - learnErrorAvgList[i] for i in xrange(len(learnErrorAvgList))]
    testDistMax     = [testErrorMaxList[i]  - testErrorAvgList[i]  for i in xrange(len(testErrorAvgList))]

    barLearnErrorAvg    = ax.bar(index,             learnErrorAvgList,  barWidth, color='r', yerr=[learnDistMin, learnDistMax])
    barTestErrorAvg     = ax.bar(index+barWidth,    testErrorAvgList,   barWidth, color='y', yerr=[testDistMin,  testDistMax])

    # add some text for labels, title and axes ticks
    title = 'Learning algorithms accuracy'
    if (isNormalizedData):
        title += " (normalized data)"
    ax.set_ylabel('Error rate')
    ax.set_title(title)
    ax.set_xticks(index + barWidth)
    ax.set_xticklabels(algoNameList)

    ax.legend((barLearnErrorAvg[0], barTestErrorAvg[0]), ('Learning error', 'Test error'))

    def autolabel(rects):
        # attach some text labels
        for rect in rects:
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width()/2., 1.05*height, '%f' % float(height), ha='center', va='bottom')

    autolabel(barLearnErrorAvg)
    autolabel(barTestErrorAvg)
    
#    plt.margins(.2)
    plt.ylim(-0.1, 1.2)  
    plt.show()


def printComparison(learnErrorMinList, learnErrorMaxList, learnErrorAvgList, testErrorMinList, testErrorMaxList, testErrorAvgList):
    print "\n\n\n\n\n"
    print "Min Learn : " + str(learnErrorMinList)
    print "Min Test  : " + str(testErrorMinList)
    print "Avg Learn : " + str(learnErrorAvgList)
    print "Avg Test  : " + str(testErrorAvgList)
    print "Max Learn : " + str(learnErrorMaxList)
    print "Max Test  : " + str(testErrorMaxList)


if __name__ == "__main__":
    if (PARAMETER_CLEAN_SAMPLE in sys.argv[1:]):
        cleanSample()
        sys.exit()

    problemInstance = ProblemInstance()
    problemInstance.parseProblemInstance(PATH_LEARNING_ALGO, PATH_TEST_SET)
    problemInstance.buildSample(LEARNING_SAMPLE_PROPORTION, PATH_TEST_SET, PATH_SAMPLE_LEARN, PATH_SAMPLE_TEST, True, PATH_TEST_SET_NORMALIZED, PATH_SAMPLE_LEARN_NORMALIZED, PATH_SAMPLE_TEST_NORMALIZED)

    if (PARAMETER_TEST_SAMPLE in sys.argv[1:]):
        testSample()
        sys.exit()

    isNormalizedData = PARAMETER_NORMALIZED_DATA in sys.argv[1:]
    if (isNormalizedData):
        (learnErrorMinList, learnErrorMaxList,  learnErrorAvgList,
         testErrorMinList,  testErrorMaxList,   testErrorAvgList)   = problemInstance.computeLearnError(PATH_PROGRAM, PATH_SAMPLE_LEARN_NORMALIZED, PATH_SAMPLE_TEST_NORMALIZED, PATH_PARAMETER, PATH_PROGRAM_OUTPUT)
    else:
        (learnErrorMinList, learnErrorMaxList,  learnErrorAvgList,
         testErrorMinList,  testErrorMaxList,   testErrorAvgList)   = problemInstance.computeLearnError(PATH_PROGRAM, PATH_SAMPLE_LEARN, PATH_SAMPLE_TEST, PATH_PARAMETER, PATH_PROGRAM_OUTPUT)

    printComparison(learnErrorMinList, learnErrorMaxList, learnErrorAvgList, testErrorMinList, testErrorMaxList, testErrorAvgList)
    plotBarComparison(problemInstance.getNbrLearningAlgo(), isNormalizedData, learnErrorMinList, learnErrorMaxList, learnErrorAvgList, testErrorMinList, testErrorMaxList, testErrorAvgList, problemInstance.getLearningAlgoNameList())

