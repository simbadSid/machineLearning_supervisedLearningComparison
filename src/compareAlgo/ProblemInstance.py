import os
from util import * 
from fileinput import close
import subprocess






class ProblemInstance:
    # -----------------------------
    # Attributes
    # -----------------------------
    """
    learningAlgoName   = []        # List of learning algo names:
    testSetName        = []        # List test sample names:
    """

    # -----------------------------
    # Builder
    # -----------------------------
    def parseProblemInstance(self, learningAlgoPath, testSetPath):
        self.learningAlgoPath   = learningAlgoPath
        self.learningAlgoName   = os.listdir(learningAlgoPath)
        self.testSetName        = os.listdir(testSetPath)


    # -----------------------------
    # Getter
    # -----------------------------
    def getNbrLearningAlgo(self):
        return len(self.learningAlgoName)

    def getNbrTestSet(self):
        return len(self.testSetName)

    def getTestSetName(self, testSetIndex):
        return self.testSetName[testSetIndex]

    def getLearningAlgoName(self, learningAlgoIndex):
        return self.learningAlgoName[learningAlgoIndex]

    def getLearningAlgoNameList(self):
        return self.learningAlgoName


    # -----------------------------
    # Local methods
    # -----------------------------
    def buildSample(self, learningSampleProportion, pathSampleRow, pathSampleLearn, pathSampleTest, buildNormalizedSample=False, pathSampleRowNormalized=None, pathSampleLearnNormalized=None, pathSampleTestNormalized=None, sampleSeparationInputChar=',', sampleSeparationChar=' '):
        if (buildNormalizedSample == True):
            for testSet in self.testSetName:
                fileNormalized  = open(pathSampleRowNormalized+testSet, 'w')
                fileRow         = open(pathSampleRow+testSet, 'r')
                while (not isEndOfFile(fileRow)):                                                                   # For each sample of the test set:
                    sample = nextMeaningLine(fileRow).split(sampleSeparationChar)                                   #    Read the sample
                    sample = normalizeSample(sample)
                    writeSample(sample, fileNormalized, sampleSeparationChar)

                fileNormalized.close()
                fileRow.close()

        for testSet in self.testSetName:                                                                            # For each test file
            swapFileLines(learningSampleProportion, testSet, pathSampleRow, pathSampleLearn, pathSampleTest);       #    Swap randomly into two distinct files
            if (buildNormalizedSample == True):
                    swapFileLines(learningSampleProportion, testSet, pathSampleRowNormalized, pathSampleLearnNormalized, pathSampleTestNormalized);


    def computeErrorAlgo(self, algo, testSet, pathProgram, pathSample_learn, pathSample_test, pathParameter, pathProgramOutput):
        progFile_learn  = pathProgram + algo + "-learn"
        progFile_test   = pathProgram + algo + "-test"
        sampleFile_learn= pathSample_learn + testSet
        sampleFile_test = pathSample_test  + testSet
        parameterFile   = pathParameter + algo
        progOutputFile  = pathProgramOutput + algo

        subprocess.call([progFile_learn, sampleFile_learn, parameterFile, progOutputFile])
        file        = open(progOutputFile)
        error_learn = float(nextMeaningLine(file))
        file.close()

        subprocess.call([progFile_test, sampleFile_test, parameterFile, progOutputFile])
        file        = open(progOutputFile)
        error_test  = float(nextMeaningLine(file))
        file.close()

        return (error_learn, error_test)

    def computeLearnError(self, pathProgram, pathSample_learn, pathSample_test, pathParameter, pathProgramOutput):
        (errorMinList_learn,    errorMaxList_learn, errorAvgList_learn) = ([], [], [])
        (errorMinList_test,     errorMaxList_test,  errorAvgList_test)  = ([], [], [])
        for algo in self.learningAlgoName:
            errorMin_learn    = None
            errorMin_test     = None
            errorMax_learn    = None
            errorMax_test     = None
            errorAvg_learn    = 0
            errorAvg_test     = 0
            for testSet in self.testSetName:
                (error_learn, error_test) = self.computeErrorAlgo(algo, testSet, pathProgram, pathSample_learn, pathSample_test, pathParameter, pathProgramOutput)
                errorAvg_learn  += error_learn
                errorAvg_test   += error_test
                if (errorMin_learn == None or error_learn < errorMin_learn):
                    errorMin_learn = error_learn
                if (errorMin_test == None or error_test < errorMin_test):
                    errorMin_test = error_test
                if (errorMax_learn == None or error_learn > errorMax_learn):
                    errorMax_learn = error_learn
                if (errorMax_test == None or error_test > errorMax_test):
                    errorMax_test = error_test
            errorMinList_learn.append(errorMin_learn)
            errorMinList_test.append(errorMin_test)
            errorMaxList_learn.append(errorMax_learn)
            errorMaxList_test.append(errorMax_test)
            errorAvgList_learn.append(errorAvg_learn / self.getNbrTestSet())
            errorAvgList_test.append(errorAvg_test / self.getNbrTestSet())

        return (errorMinList_learn, errorMaxList_learn,  errorAvgList_learn,
                errorMinList_test, errorMaxList_test,  errorAvgList_test)