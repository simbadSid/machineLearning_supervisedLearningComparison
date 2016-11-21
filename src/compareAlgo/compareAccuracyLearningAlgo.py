from ProblemInstance import ProblemInstance
from util import *
import sys
import os
import numpy as np
import matplotlib.pyplot as plt




PARAMETER_HELP                 = "-help"
PARAMETER_TEST_SAMPLE          = "-testSample"
PARAMETER_BUILD_SAMPLE         = "-buildSample"
PARAMETER_CLEAN_SAMPLE         = "-clean"
PARAMETER_NORMALIZED_DATA      = "-normalized"
PARAMETER_STANDARD_DEVIATION   = "-standardDeviation"

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
NBR_STANDARD_DEVIATION_RUN     = 4




def help():
    print "\t" + "<No argument>"                + "\t: Run the train and test of the learning algorithm on the existing data: " + PATH_TEST_SET
    print "\t" + PARAMETER_TEST_SAMPLE          + "\t: To test the validity of the built samples (normalization, uniformity of the swap probability)"
    print "\t" + PARAMETER_BUILD_SAMPLE         + "\t: To build the learn and test samples (based on a fixed set of samples)"
    print "\t" + PARAMETER_CLEAN_SAMPLE         + "\t\t: Remove all the created learn and test samples"
    print "\t" + PARAMETER_NORMALIZED_DATA      + "\t: Use the normalized data for the training and the testing of the learning algorithms"
    print "\t" + PARAMETER_STANDARD_DEVIATION   + "\t: Computes the standard deviation of the learn and test error"


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


def runStandardDeviationTest(isNormalizedData, problemInstance):
#TODO: replace the hole content of the function by an addaptation of problemInstance.computeLearnError
#TODO: adapt the plot function
    (learnErrorMinListList, learnErrorMaxListList,  learnErrorAvgListList, testErrorMinListList,  testErrorMaxListList,   testErrorAvgListList) = ([], [], [], [], [], [])
    for i in xrange(NBR_STANDARD_DEVIATION_RUN):
        if (isNormalizedData):
            (learnErrorMinList, learnErrorMaxList,  learnErrorAvgList,
             testErrorMinList,  testErrorMaxList,   testErrorAvgList)   = problemInstance.computeLearnError(PATH_PROGRAM, PATH_SAMPLE_LEARN_NORMALIZED, PATH_SAMPLE_TEST_NORMALIZED, PATH_PARAMETER, PATH_PROGRAM_OUTPUT)
        else:
            (learnErrorMinList, learnErrorMaxList,  learnErrorAvgList,
             testErrorMinList,  testErrorMaxList,   testErrorAvgList)   = problemInstance.computeLearnError(PATH_PROGRAM, PATH_SAMPLE_LEARN, PATH_SAMPLE_TEST, PATH_PARAMETER, PATH_PROGRAM_OUTPUT)
        learnErrorMinListList   .append(learnErrorMinList)
        learnErrorMaxListList   .append(learnErrorMaxList)
        learnErrorAvgListList   .append(learnErrorAvgList)
        testErrorMinListList    .append(testErrorMinList)
        testErrorMaxListList    .append(testErrorMaxList)
        testErrorAvgListList    .append(testErrorAvgList)

    learnErrorMinMean   = [x / NBR_STANDARD_DEVIATION_RUN for x in learnErrorMinListList[0]]  
    learnErrorMaxMean   = [x / NBR_STANDARD_DEVIATION_RUN for x in learnErrorMaxListList[0]]
    learnErrorAvgMean   = [x / NBR_STANDARD_DEVIATION_RUN for x in learnErrorAvgListList[0]]
    testErrorMinMean    = [x / NBR_STANDARD_DEVIATION_RUN for x in testErrorMinListList[0]]
    testErrorMaxMean    = [x / NBR_STANDARD_DEVIATION_RUN for x in testErrorMaxListList[0]]
    testErrorAvgMean    = [x / NBR_STANDARD_DEVIATION_RUN for x in testErrorAvgListList[0]]
    N = len(learnErrorMinListList[0])
    for i in range(1, NBR_STANDARD_DEVIATION_RUN):
        learnErrorMinMean   = [learnErrorMinMean[j] + learnErrorMinListList[i][j] / NBR_STANDARD_DEVIATION_RUN for j in xrange(N)]
        learnErrorMaxMean   = [learnErrorMaxMean[j] + learnErrorMaxListList[i][j] / NBR_STANDARD_DEVIATION_RUN for j in xrange(N)]
        learnErrorAvgMean   = [learnErrorAvgMean[j] + learnErrorAvgListList[i][j] / NBR_STANDARD_DEVIATION_RUN for j in xrange(N)]
        testErrorMinMean    = [testErrorMinMean[j]  + testErrorMinListList[i][j]  / NBR_STANDARD_DEVIATION_RUN for j in xrange(N)]
        testErrorMaxMean    = [testErrorMaxMean[j]  + testErrorMaxListList[i][j]  / NBR_STANDARD_DEVIATION_RUN for j in xrange(N)]
        testErrorAvgMean    = [testErrorAvgMean[j]  + testErrorAvgListList[i][j]  / NBR_STANDARD_DEVIATION_RUN for j in xrange(N)]

    for i in xrange(NBR_STANDARD_DEVIATION_RUN):
        learnErrorMinListList[i] = [math.pow(learnErrorMinListList[i][j] - learnErrorMinMean[j], 2) for j in xrange(N)]
        learnErrorMaxListList[i] = [math.pow(learnErrorMaxListList[i][j] - learnErrorMaxMean[j], 2) for j in xrange(N)]
        learnErrorAvgListList[i] = [math.pow(learnErrorAvgListList[i][j] - learnErrorAvgMean[j], 2) for j in xrange(N)]
        testErrorMinListList[i]  = [math.pow(testErrorMinListList[i][j]  - testErrorMinMean[j], 2) for j in xrange(N)]
        testErrorMaxListList[i]  = [math.pow(testErrorMaxListList[i][j]  - testErrorMaxMean[j], 2) for j in xrange(N)]
        testErrorAvgListList[i]  = [math.pow(testErrorAvgListList[i][j]  - testErrorAvgMean[j], 2) for j in xrange(N)]

    learnErrorMinMean   = [x / NBR_STANDARD_DEVIATION_RUN for x in learnErrorMinListList[0]]  
    learnErrorMaxMean   = [x / NBR_STANDARD_DEVIATION_RUN for x in learnErrorMaxListList[0]]
    learnErrorAvgMean   = [x / NBR_STANDARD_DEVIATION_RUN for x in learnErrorAvgListList[0]]
    testErrorMinMean    = [x / NBR_STANDARD_DEVIATION_RUN for x in testErrorMinListList[0]]
    testErrorMaxMean    = [x / NBR_STANDARD_DEVIATION_RUN for x in testErrorMaxListList[0]]
    testErrorAvgMean    = [x / NBR_STANDARD_DEVIATION_RUN for x in testErrorAvgListList[0]]
    for i in range(1, NBR_STANDARD_DEVIATION_RUN):
        learnErrorMinMean   = [learnErrorMinMean[j] + learnErrorMinListList[i][j] / NBR_STANDARD_DEVIATION_RUN for j in xrange(N)]
        learnErrorMaxMean   = [learnErrorMaxMean[j] + learnErrorMaxListList[i][j] / NBR_STANDARD_DEVIATION_RUN for j in xrange(N)]
        learnErrorAvgMean   = [learnErrorAvgMean[j] + learnErrorAvgListList[i][j] / NBR_STANDARD_DEVIATION_RUN for j in xrange(N)]
        testErrorMinMean    = [testErrorMinMean[j]  + testErrorMinListList[i][j]  / NBR_STANDARD_DEVIATION_RUN for j in xrange(N)]
        testErrorMaxMean    = [testErrorMaxMean[j]  + testErrorMaxListList[i][j]  / NBR_STANDARD_DEVIATION_RUN for j in xrange(N)]
        testErrorAvgMean    = [testErrorAvgMean[j]  + testErrorAvgListList[i][j]  / NBR_STANDARD_DEVIATION_RUN for j in xrange(N)]
        
    printComparison(learnErrorMinMean, learnErrorMaxMean, learnErrorAvgMean, testErrorMinMean, testErrorMaxMean, testErrorAvgMean)
    plotBarComparison(problemInstance.getNbrLearningAlgo(), isNormalizedData, learnErrorMinMean, learnErrorMaxMean, learnErrorAvgMean, testErrorMinMean, testErrorMaxMean, testErrorAvgMean, problemInstance.getLearningAlgoNameList())


def runErrorTest(isNormalizedData, problemInstance):
    if (isNormalizedData):
        (learnErrorMinList, learnErrorMaxList,  learnErrorAvgList,
         testErrorMinList,  testErrorMaxList,   testErrorAvgList)   = problemInstance.computeLearnError(PATH_PROGRAM, PATH_SAMPLE_LEARN_NORMALIZED, PATH_SAMPLE_TEST_NORMALIZED, PATH_PARAMETER, PATH_PROGRAM_OUTPUT)
    else:
        (learnErrorMinList, learnErrorMaxList,  learnErrorAvgList,
         testErrorMinList,  testErrorMaxList,   testErrorAvgList)   = problemInstance.computeLearnError(PATH_PROGRAM, PATH_SAMPLE_LEARN, PATH_SAMPLE_TEST, PATH_PARAMETER, PATH_PROGRAM_OUTPUT)

    """
    MinLearn = [0.0032294168571875004, 0.0, 0.0114810996771875]
    MinTest  = [0.0024059565931875003, 0.0, 0.00010140778799999998]
    AvgLearn = [0.003592956637386721, 5.813812499999201e-09, 0.006562060892218751]
    AvgTest  = [0.005131343134449218, 3.823886718750195e-09, 3.0266668578124942e-05]
    MaxLearn = [0.007202637817250002, 9.302099999999783e-08, 0.053046189891999995]
    MaxTest  = [0.008975204876687497, 6.118218749999945e-08, 8.160576875000068e-07]
    """
    printComparison(learnErrorMinList, learnErrorMaxList, learnErrorAvgList, testErrorMinList, testErrorMaxList, testErrorAvgList)
    plotBarComparison(problemInstance.getNbrLearningAlgo(), isNormalizedData, learnErrorMinList, learnErrorMaxList, learnErrorAvgList, testErrorMinList, testErrorMaxList, testErrorAvgList, problemInstance.getLearningAlgoNameList())


if __name__ == "__main__":
    if (PARAMETER_HELP in sys.argv[1:]):
        help()
        sys.exit()

    if (PARAMETER_CLEAN_SAMPLE in sys.argv[1:]):
        cleanSample()
        sys.exit()

    isNormalizedData= PARAMETER_NORMALIZED_DATA in sys.argv[1:]
    problemInstance = ProblemInstance()
    problemInstance.parseProblemInstance(PATH_LEARNING_ALGO, PATH_TEST_SET)
    if (PARAMETER_BUILD_SAMPLE in sys.argv[1:]):
        problemInstance.buildSample(LEARNING_SAMPLE_PROPORTION, PATH_TEST_SET, PATH_SAMPLE_LEARN, PATH_SAMPLE_TEST, True, PATH_TEST_SET_NORMALIZED, PATH_SAMPLE_LEARN_NORMALIZED, PATH_SAMPLE_TEST_NORMALIZED)
        sys.exit()

    if (PARAMETER_TEST_SAMPLE in sys.argv[1:]):
        testSample()
        sys.exit()

    if (PARAMETER_STANDARD_DEVIATION in sys.argv[1:]):
        runStandardDeviationTest(isNormalizedData, problemInstance)
    else:
        runErrorTest(isNormalizedData, problemInstance)

