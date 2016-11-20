EXEC			= adaBoost-test adaBoost-learn logisticRegression-test logisticRegression-learn perceptron-test perceptron-learn ####multilayerPerceptron-learn multilayerPerceptron-test
CC				= gcc
CFLAGS 			= -g #-Wall -Werror
LIB				= -lm
src				= learningAlgo
bin				= ../bin

printerCancel	= -I../util/customPrinter.h #-Dprintf=cancelPrint_standardOutput

all : $(EXEC)






#------------------------------------------------------------------------------------------------------------
#----------------------------------------- Executables ------------------------------------------------------
#------------------------------------------------------------------------------------------------------------
perceptron-learn: $(bin)/util/customPrinter.o $(bin)/perceptron/utilitaire.o $(bin)/perceptron/perceptron.o $(bin)/perceptron/perceptron-learn-main.o
	$(CC) $(CFLAGS) -o $@ $^

perceptron-test: $(bin)/util/customPrinter.o $(bin)/perceptron/utilitaire.o $(bin)/perceptron/perceptron-test.o
	$(CC) $(CFLAGS) -o $@ $^

multilayerPerceptron-learn: $(bin)/util/customPrinter.o $(bin)/multilayerPerceptron/MLP_BackProp.o $(bin)/multilayerPerceptron/utilitaire.o $(bin)/multilayerPerceptron/MLP-Learn.o
	$(CC) $(CFLAGS) -o $@ $^ $(LIB)

multilayerPerceptron-test: $(bin)/util/customPrinter.o $(bin)/multilayerPerceptron/Propagation.o $(bin)/multilayerPerceptron/utilitaire.o $(bin)/multilayerPerceptron/MLP-Test.o
	$(CC) $(CFLAGS) -o $@ $^ $(LIB)

logisticRegression-learn: $(bin)/util/customPrinter.o $(bin)/logisticRegression/utilitaire.o $(bin)/logisticRegression/Optimiseurs.o $(bin)/logisticRegression/LogisticRegression-learn.o $(bin)/logisticRegression/LogisticRegression-learn-main.o
	$(CC) $(CFLAGS) -o $@ $^ $(LIB)

logisticRegression-test: $(bin)/util/customPrinter.o $(bin)/logisticRegression/utilitaire.o $(bin)/logisticRegression/LogisticRegression-test.o
	$(CC) $(CFLAGS) -o $@ $^ $(LIB)

adaBoost-learn: $(bin)/util/customPrinter.o $(bin)/adaBoost/utilitaire.o $(bin)/adaBoost/Optimiseurs.o $(bin)/adaBoost/perceptron.o $(bin)/adaBoost/LogisticRegression-learn.o $(bin)/adaBoost/AdaBoost-learn.o $(bin)/adaBoost/AdaBoost-learn-main.o
	$(CC) $(CFLAGS) -o $@ $^ $(LIB)

adaBoost-test: $(bin)/util/customPrinter.o $(bin)/adaBoost/utilitaire.o $(bin)/adaBoost/AdaBoost-test.o
	$(CC) $(CFLAGS) -o $@ $^ $(LIB)



#-----------------------------------------------------------------------------------------------------------
#---------------------------------------- Binaries ---------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------
$(bin)/adaBoost/%.o 			: $(src)/adaBoost/%.c
								$(CC) $(CFLAGS) -c -o $@ $(printerCancel) $^

$(bin)/logisticRegression/%.o 	: $(src)/logisticRegression/%.c
								$(CC) $(CFLAGS) -c -o $@ $(printerCancel) $^

$(bin)/multilayerPerceptron/%.o : $(src)/multilayerPerceptron/%.c
								$(CC) $(CFLAGS) -c -o $@ $(printerCancel) $^

$(bin)/perceptron/%.o 			: $(src)/perceptron/%.c
								$(CC) $(CFLAGS) -c -o $@ $(printerCancel) $^

$(bin)/util/%.o 				: util/%.c
								$(CC) $(CFLAGS) -c -o $@ $^


#-----------------------------------------------------------------------------------------------------------
#---------------------------------------- General Methodes -------------------------------------------------
#-----------------------------------------------------------------------------------------------------------
.PHONY	: clean mrproper
clean:	#$(EXEC)
		rm -f -r $(bin)/*/*.o
mrproper: clean
		rm -rf $(EXEC)



