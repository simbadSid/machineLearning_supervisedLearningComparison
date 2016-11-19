import os
from util import * 
from fileinput import close






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
        self.learningAlgoName   = os.listdir(learningAlgoPath);
        self.testSetName        = os.listdir(testSetPath)


    # -----------------------------
    # Getter
    # -----------------------------
    def getNbrLearningAlgo(self):
        return len(self.learningAlgoName)

    def getNbrTestSet(self):
        return len(self.testSetName)

    def getLearningAlgoName(self, learningAlgoIndex):
        return self.learningAlgoName[learningAlgoIndex]

    def getTestSetName(self, testSetIndex):
        return self.testSetName[testSetIndex]


    # -----------------------------
    # Local methods
    # -----------------------------
    def buildSample(self, learningSampleProportion, pathSampleRow, pathSampleLearn, pathSampleTest, buildNormalizedSample=False, pathSampleRowNormalized=None, pathSampleLearnNormalized=None, pathSampleTestNormalized=None, sampleSeparationChar=','):
        if (buildNormalizedSample == True):
            for testSet in self.testSetName:
                fileNormalized  = open(pathSampleRowNormalized+testSet, 'w')
                fileRow         = open(pathSampleRow+testSet, 'r')
                while (not isEndOfFile(fileRow)):                                                               # For each sample of the test set:
                    sample = nextMeaningLine(fileRow).split(sampleSeparationChar)                               #    Read the sample
                    sample = normalizeSample(sample)
                    fileNormalized.write(str(sample) + "\n")

                fileNormalized.close()
                fileRow.close()

        for testSet in self.testSetName:                                                                        # For each test file
            swapFileLines(learningSampleProportion, testSet, pathSampleRow, pathSampleLearn, pathSampleTest);   #    Swap randomly into two distinct files
            if (buildNormalizedSample == True):
                    swapFileLines(learningSampleProportion, testSet, pathSampleRowNormalized, pathSampleLearnNormalized, pathSampleTestNormalized);
