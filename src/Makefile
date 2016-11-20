EXEC	= adaBoost-test adaBoost-learn logisticRegression-test logisticRegression-learn perceptron-test perceptron-learn ####multilayerPerceptron-learn multilayerPerceptron-test
CC		= gcc
CFLAGS 	= -g #-Wall -Werror
LIB		= -lm
src		= learningAlgo
bin		= ../bin

all : $(EXEC)






#------------------------------------------------------------------------------------------------------------
#----------------------------------------- Executables ------------------------------------------------------
#------------------------------------------------------------------------------------------------------------
perceptron-learn: $(bin)/perceptron/utilitaire.o $(bin)/perceptron/perceptron.o $(bin)/perceptron/perceptron-learn-main.o
	$(CC) $(CFLAGS) -o $@ $^

perceptron-test: $(bin)/perceptron/utilitaire.o $(bin)/perceptron/perceptron-test.o
	$(CC) $(CFLAGS) -o $@ $^

multilayerPerceptron-learn: $(bin)/multilayerPerceptron/MLP_BackProp.o $(bin)/multilayerPerceptron/utilitaire.o $(bin)/multilayerPerceptron/MLP-Learn.o
	$(CC) $(CFLAGS) -o $@ $^ $(LIB)

multilayerPerceptron-test: $(bin)/multilayerPerceptron/Propagation.o $(bin)/multilayerPerceptron/utilitaire.o $(bin)/multilayerPerceptron/MLP-Test.o
	$(CC) $(CFLAGS) -o $@ $^ $(LIB)

logisticRegression-learn: $(bin)/logisticRegression/utilitaire.o $(bin)/logisticRegression/Optimiseurs.o $(bin)/logisticRegression/LogisticRegression-learn.o $(bin)/logisticRegression/LogisticRegression-learn-main.o
	$(CC) $(CFLAGS) -o $@ $^ $(LIB)

logisticRegression-test: $(bin)/logisticRegression/utilitaire.o $(bin)/logisticRegression/LogisticRegression-test.o
	$(CC) $(CFLAGS) -o $@ $^ $(LIB)

adaBoost-learn: $(bin)/adaBoost/utilitaire.o $(bin)/adaBoost/Optimiseurs.o $(bin)/adaBoost/perceptron.o $(bin)/adaBoost/LogisticRegression-learn.o $(bin)/adaBoost/AdaBoost-learn.o $(bin)/adaBoost/AdaBoost-learn-main.o
	$(CC) $(CFLAGS) -o $@ $^ $(LIB)

adaBoost-test: $(bin)/adaBoost/utilitaire.o $(bin)/adaBoost/AdaBoost-test.o
	$(CC) $(CFLAGS) -o $@ $^ $(LIB)



#-----------------------------------------------------------------------------------------------------------
#---------------------------------------- Binaries ---------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------
$(bin)/adaBoost/%.o 			: $(src)/adaBoost/%.c
								$(CC) $(CFLAGS) -c -o $@ $^

$(bin)/logisticRegression/%.o 	: $(src)/logisticRegression/%.c
								$(CC) $(CFLAGS) -c -o $@ $^

$(bin)/multilayerPerceptron/%.o : $(src)/multilayerPerceptron/%.c
								$(CC) $(CFLAGS) -c -o $@ $^

$(bin)/perceptron/%.o 			: $(src)/perceptron/%.c
								$(CC) $(CFLAGS) -c -o $@ $^


#-----------------------------------------------------------------------------------------------------------
#---------------------------------------- General Methodes -------------------------------------------------
#-----------------------------------------------------------------------------------------------------------
.PHONY	: clean mrproper
clean:	#$(EXEC)
		rm -f -r $(bin)/*/*.o
mrproper: clean
		rm -rf $(EXEC)



