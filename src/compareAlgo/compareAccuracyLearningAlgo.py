from ProblemInstance import ProblemInstance
from util import *
import sys
import os





PARAMETER_TEST_SAMPLE          = "testSample"
PARAMETER_CLEAN_SAMPLE         = "clean"

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

    (learnErrorMinList, learnErrorMaxList,  learnErrorAvgList,
     testErrorMinList,  testErrorMaxList,   testErrorAvgList)   = problemInstance.computeLearnError(PATH_PROGRAM, PATH_SAMPLE_LEARN_NORMALIZED, PATH_SAMPLE_TEST_NORMALIZED, PATH_PARAMETER, PATH_PROGRAM_OUTPUT)


