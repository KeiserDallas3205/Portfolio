/*
Name: Keiser Dallas
Date: 10/20/2023
Class: CSC 475-001
Assignment 2
Desc: This program is a fully-connected, feed forward neural network with stochastic gradient descent and back
            propagation that uses data from the MNIST database to solve the handwritten digit problem. The
            neural network has the following architecture:
                HIDDEN LAYER -> 100 nodes
                OUTPUT LAYER -> 10 nodes
            Furthermore, the program has a menu that allows the user to navigate train and test the network easier.
            so that you can continuously train a network, and then display the accuracy results when needed.
            Finally, it has 2 different modes that allow you to actively watch the network classify digits.
            Furthermore, it can load a pre-trained network state, and save the current network state to a
            pre-destined file path.
 */

import java.io.FileNotFoundException;
import java.lang.Math;
import java.util.Random;
import java.util.Arrays;
import java.util.Scanner;
import java.io.File;
import java.io.FileWriter;
import java.io.BufferedWriter;

public class Network {

    //region ************ NETWORK SETUP ************
    // CONSTANTS
    public static final int EPOCHS = 30;
    public static final int BATCH_SIZE = 10;
    public static final int NUM_BATCHES = 2;
    public static final double LEARNING_RATE = 3;

    // INPUTS & CLASSIFICATIONS
    public static double[][] trainingInputs = new double[60000][784];

    public static int[][] trainingTargets = new int[60000][10];

    public static double[][] testingInputs = new double[10000][784];

    public static int[][] testingTargets = new int[10000][10];



    // LAYER 1
    public static double[][] weightsInputHidden = randomize(new double[100][784]);

    public static double[][] hiddenBias = randomize(new double[100][1]);
    public static double[][] hiddenLayerOutput = new double[100][1];

    public static double[][] sumHiddenWeightGradient = new double[100][784];

    public static double[][] sumHiddenBiasGradient = new double[100][1];

    // LAYER 2

    public static double[][] weightsHiddenOutput = randomize(new double[10][100]);
    public static double[][] outputBias = randomize(new double[10][1]);


    public static double[][] sumOutputWeightGradient = new double[10][784];

    public static double[][] sumOutputBiasGradient = new double[10][1];

    // NETWORK ACCURACY
    public static int total = 0;
    public static int[] digitTotal = {0,0,0,0,0,0,0,0,0,0};
    public static int correct = 0;
    public static int[] digitCorrect = {0,0,0,0,0,0,0,0,0,0};

    // MENU
    public static String firstMenu = "\n[1] Train the network\n[2] Load pre-trained network\n[0] Exit";
    public static String secondMenu = "\n[1] Train the network\n[2] Load pre-trained network\n[3] Display network accuracy on TRAINING data\n[4] Display network accuracy on TESTING data\n[5] Run network on TESTING data showing images and labels\n[6] Display the misclassified TESTING images\n[7] Save the network state to a file\n[0] Exit";


    //endregion




    //region ********** ENGINE ********************
    public static void main(String[] args)
    {
        // Load training & testing data
        System.out.println("Loading data...\n");
        readData("data/mnist_train.csv", trainingInputs,trainingTargets);
        readData("data/mnist_test.csv", testingInputs,testingTargets);



        // START OF MENU
        Scanner userListener = new Scanner(System.in);

        // Display the first menu
        System.out.println(firstMenu);

        // Allow user to traverse the program
        while(true) {
            // Get user response
            int answer = userListener.nextInt();

            switch(answer) {
                // Train the network
                case 1:
                    train(trainingInputs, trainingTargets);

                    break;
                // Load a pre-trained network
                case 2:
                    loadNetwork();
                    break;

                // Display network accuracy on TRAINING data
                case 3:
                    test(trainingInputs,trainingTargets);
                    break;

                //  Display network accuracy on TESTING data
                case 4:
                    test(testingInputs,testingTargets);
                    break;

                //  Run network on TESTING data showing images and labels
                case 5:
                    testShow(testingInputs,testingTargets);
                    break;

                // Display the misclassified TESTING images
                case 6:
                    testShowIncorrect(testingInputs,testingTargets);
                    break;

                // Save the network state to file
                case 7:
                    saveNetwork();
                    break;

                // Exit the program
                case 0:
                    System.out.println("Exiting...\n");
                    System.exit(0);
            }
            System.out.println(secondMenu);
        }
        
    }

    //endregion


    //region *********** NETWORK FUNCTIONS *********
    // Function takes in ALL TRAINING inputs, and ALL TRAINING targets
    // Splits the inputs into MINI-BATCHES
    // Runs forward & backward pass on each input in network
    // Updates the weights & biases AFTER each MINI-BATCH
    //      FLUSHES gradients afterwards
    static void train(double[][] input, int[][] target)
    {
        // Reset your counters
        correct = 0;
        total = 0;
        reset(digitTotal);
        reset(digitCorrect);

        System.out.println("\nTraining network...\n");
        for(int i = 0; i < EPOCHS;i++)
        {
            System.out.print(String.format("EPOCH: %d\n", i+1));

            // Randomize the mini-batches
            int[] randIndices = scramble(60000);

            // For each input
            int j = 0;
            int k = 1;
            while(j < input.length)
            {
                // Process the input
                backProp(feedForward(convert2(input[randIndices[j]])), convert(target[randIndices[j]]), convert2(input[randIndices[j]]),k);

                j += 1;
                k += 1;
            }
            // Display NETWORK ACCURACY
            showAccuracy();
            // Reset your counters
            correct = 0;
            total = 0;
            reset(digitTotal);
            reset(digitCorrect);


        }
    }

    // Function takes in ALL TESTING inputs, and ALL TESTING targets
    // Using the current weights & biases of the networks,
    //      it tests the network on TESTING DATA
    //      Then it displays its accuracy
    static void test(double[][] input, int[][] target)
    {
        System.out.println("\nTesting network...");
        // Reset your counters again
        correct = 0;
        total = 0;
        reset(digitTotal);
        reset(digitCorrect);



        // For each input
        int i = 0;
        int k = 1;
        while(i < input.length)
        {
            total += 1;
            digitTotal[check(convert(target[i]))] += 1;
            // If correct
            if(check2(feedForward(convert2(input[i]))) == check(convert(target[i])))
            {
                correct += 1;
                digitCorrect[ check(convert(target[i]))] += 1;
            }


            i += 1;
            k += 1;
        }
        // Display NETWORK ACCURACY
        showAccuracy();

        // Reset your counters again
        correct = 0;
        total = 0;
        reset(digitTotal);
        reset(digitCorrect);

    }


    // Function takes in ALL TESTING inputs, and ALL TESTING targets
    // Using the current weights & biases of the networks,
    //      it tests the network on TESTING DATA
    //      Then it displays its accuracy
    // ADDITIONALLY SHOWS IMAGES AS IT IS TESTING
    static void testShow(double[][] input, int[][] target)
    {
        Scanner scanner = new Scanner(System.in);
        System.out.println("\nTesting network...");
        // Reset your counters again
        correct = 0;
        total = 0;
        reset(digitTotal);
        reset(digitCorrect);



        // For each input
        int i = 0;
        int k = 1;
        while(i < input.length)
        {

            total += 1;
            digitTotal[check(convert(target[i]))] += 1;
            String s = String.format("\nCase: %d  Correct classification = %d  Network Output = %d Incorrect\n",i,check(convert(target[i])), check2(feedForward(convert2(input[i]))));
            // If correct
            if(check2(feedForward(convert2(input[i]))) == check(convert(target[i])))
            {
                correct += 1;
                digitCorrect[ check(convert(target[i]))] += 1;
                s = String.format("\nCase: %d  Correct classification = %d  Network Output = %d Correct\n",i,check(convert(target[i])), check2(feedForward(convert2(input[i]))));
            }



            // DISPLAY THE IMAGE
            System.out.println(s);
            printImage(pixelate(input[i]));
            System.out.println("\nEnter [1] to continue, or [0] to go back to menu\n");
            int answer = scanner.nextInt();
            if(answer == 0)
            {
                return;
            }



            i += 1;
            k += 1;
        }
        // Display NETWORK ACCURACY
        showAccuracy();

        // Reset your counters again
        correct = 0;
        total = 0;
        reset(digitTotal);
        reset(digitCorrect);
    }


    // Function takes in ALL TESTING inputs, and ALL TESTING targets
    // Using the current weights & biases of the networks,
    //      it tests the network on TESTING DATA
    //      Then it displays its accuracy
    // ADDITIONALLY SHOWS IMAGES AS IT IS TESTING (IF INCORRECT)
    static void testShowIncorrect(double[][] input, int[][] target)
    {
        Scanner scanner = new Scanner(System.in);
        System.out.println("\nTesting network...");
        // Reset your counters again
        correct = 0;
        total = 0;
        reset(digitTotal);
        reset(digitCorrect);

        // For each input
        int i = 0;
        int k = 1;
        while(i < input.length)
        {

            total += 1;
            digitTotal[check(convert(target[i]))] += 1;
            String s = String.format("\nCase: %d  Correct classification = %d  Network Output = %d Incorrect\n",i,check(convert(target[i])), check2(feedForward(convert2(input[i]))));
            // If correct
            if(check2(feedForward(convert2(input[i]))) == check(convert(target[i])))
            {
                correct += 1;
                digitCorrect[ check(convert(target[i]))] += 1;
                s = String.format("\nCase: %d  Correct classification = %d  Network Output = %d Correct\n",i,check(convert(target[i])), check2(feedForward(convert2(input[i]))));
            }



            // DISPLAY THE IMAGE (only if incorrect)
            if(check2(feedForward(convert2(input[i]))) != check(convert(target[i])))
            {
                System.out.println(s);
                printImage(pixelate(input[i]));
                System.out.println("Enter [1] to continue, or [0] to exit");
                int answer = scanner.nextInt();
                if(answer == 0)
                {
                    return;
                }
            }



            i += 1;
            k += 1;
        }
        // Display NETWORK ACCURACY
        showAccuracy();

        // Reset your counters again
        correct = 0;
        total = 0;
        reset(digitTotal);
        reset(digitCorrect);
    }


    // Function takes in an int[][], input
    // Calculates the activation of the network for that input
    // Returns the activation, double[][]
    static double[][] feedForward(double[][] input)
    {

        // Calculate activation of HIDDEN LAYER
        //double[][] hiddenLayerOutput = new double[3][1];
        // X * W
        for(int i = 0; i < weightsInputHidden.length; i++)
        {
            for(int j = 0; j < input[0].length;j++)
            {
                double product = 0.0;
                for(int k = 0; k < input.length; k++)
                {
                    product += (weightsInputHidden[i][k] * input[k][j]);
                }
                hiddenLayerOutput[i][j] = product;
            }
        }

        // + B
        for(int i = 0; i < hiddenLayerOutput.length;i++)
        {
            for(int j = 0; j < hiddenLayerOutput[i].length; j++)
            {
                hiddenLayerOutput[i][j] += hiddenBias[i][j];
            }
        }

        // Sigmoid
        for(int i = 0; i < hiddenLayerOutput.length;i++)
        {
            for(int j = 0; j < hiddenLayerOutput[i].length;j++)
            {
                hiddenLayerOutput[i][j] = sigmoid(hiddenLayerOutput[i][j]);
            }
        }

        // DEBUG
        //System.out.println("DEBUG STATEMENT 1: ACTIVATION OF HIDDEN LAYER\n");
        //print(hiddenLayerOutput);

        // Calculate activation of OUTPUT LAYER
        double[][] outputLayerOutput = new double[10][1];
        // X * W
        for(int i = 0; i < weightsHiddenOutput.length;i++)
        {
            for(int j = 0; j < hiddenLayerOutput[0].length;j++)
            {
                double product = 0.0;
                for(int k = 0; k < hiddenLayerOutput.length;k++)
                {
                    product += weightsHiddenOutput[i][k] * hiddenLayerOutput[k][j];
                }
                outputLayerOutput[i][j] = product;
            }
        }

        // + B
        for(int i = 0; i < outputLayerOutput.length;i++)
        {
            for(int j = 0; j < outputLayerOutput[0].length;j++)
            {
                outputLayerOutput[i][j] += outputBias[i][j];
            }
        }

        // Sigmoid
        for(int i = 0; i < outputLayerOutput.length;i++)
        {
            for(int j = 0; j < outputLayerOutput[0].length;j++)
            {
                outputLayerOutput[i][j] = sigmoid(outputLayerOutput[i][j]);
            }
        }

        // DEBUG
        //System.out.println("DEBUG STATEMENT 2: ACTIVATION OF OUTPUT LAYER\n");
        //print(outputLayerOutput);

        // Return activation
        return outputLayerOutput;
    }

    // Function that takes in OUTPUT LAYER activation, and desired output
    // Computes error in network
    // Returns gradient values
    static void backProp(double[][] a, int[][] target, double[][] input, int k)
    {
        // NETWORK ACCURACY
        //      Check if answer was correct
        total +=1;
        digitTotal[check(target)] += 1;
        if(check2(a) == check(target))
        {
            correct +=1;
            digitCorrect[check(target)] += 1;
        }
        // Calculate OUTPUT LAYER bias gradient
        // (A - Y) * A(1 - A)
        double[][] outputBiasGradient = new double [10][1];
        for(int i = 0; i < a.length;i++)
        {
            for(int j = 0; j < a[0].length;j++)
            {
                outputBiasGradient[i][j] = (a[i][j] - target[i][j]) * sigmoidDeriv(a[i][j]);
            }
        }

        // Summation of OUTPUT LAYER bias gradient
        for(int i = 0; i < outputBiasGradient.length;i++)
        {
            for(int j = 0; j < outputBiasGradient[i].length;j++)
            {
                sumOutputBiasGradient[i][j] += outputBiasGradient[i][j];
            }
        }

        // DEBUG
        //System.out.println("DEBUG STATEMENT 3: BIAS GRADIENT OF OUTPUT LAYER\n");
        //print(outputBiasGradient);

        // Calculate OUTPUT LAYER weight gradient
        // a * outputBiasGradient
        double[] A = transpose(hiddenLayerOutput);
        for(int i = 0; i < outputBiasGradient.length;i++)
        {
            for(int j = 0; j < A.length;j++)
            {
                sumOutputWeightGradient[i][j] += outputBiasGradient[i][0] * A[j];
            }
        }

        // DEBUG
        //System.out.println("DEBUG STATEMENT 4: WEIGHT GRADIENT OF OUTPUT LAYER\n");
        //print(sumOutputWeightGradient);



        // Calculate INPUT LAYER bias gradient
        double[][] hiddenBiasGradient = new double[100][1];
        // W * OUTPUT LAYER ERROR
        for(int i = 0; i < weightsHiddenOutput[0].length;i++)
        {
            double[] column = column(weightsHiddenOutput,i);
            double product = 0.0;
            for(int j = 0; j < column.length;j++)
            {
                product += outputBiasGradient[j][0] * column[j];
            }
            hiddenBiasGradient[i][0] = product;
        }

        // * A(1 - A)
        for(int i = 0; i < hiddenBiasGradient.length;i++)
        {
            hiddenBiasGradient[i][0] *= sigmoidDeriv(hiddenLayerOutput[i][0]);
        }

        // Summation of HIDDEN LAYER bias gradient
        for(int i = 0; i < hiddenBiasGradient.length;i++)
        {
            for(int j = 0; j < hiddenBiasGradient[i].length;j++)
            {
                sumHiddenBiasGradient[i][j] += hiddenBiasGradient[i][j];
            }
        }

        // DEBUG
        //System.out.println("DEBUG STATEMENT 5: BIAS GRADIENT OF HIDDEN LAYER\n");
        //print(hiddenBiasGradient);



        // Calculate HIDDEN LAYER weight gradient
        // input * hiddenBiasGradient

        double[] B = transpose(input);
        for(int i = 0; i < hiddenBiasGradient.length;i++)
        {
            for(int j = 0; j < B.length;j++)
            {
                sumHiddenWeightGradient[i][j] += hiddenBiasGradient[i][0] * B[j];
            }
        }

        // DEBUG
        //System.out.println("DEBUG STATEMENT 6: WEIGHT GRADIENT OF HIDDEN LAYER\n");
        //print(sumHiddenWeightGradient);

        // UPDATE WEIGHTS
        // ONLY AFTER MINI-BATCH
        if(k!= 0 && k % BATCH_SIZE == 0)
        {
            // Update HIDDEN LAYER weights
            update(weightsInputHidden, sumHiddenWeightGradient);

            // DEBUG
            //System.out.println("DEBUG STATEMENT 7: NEW HIDDEN LAYER WEIGHTS\n");
            //print(weightsInputHidden);

            // Update HIDDEN LAYER bias
            update(hiddenBias,sumHiddenBiasGradient);

            // DEBUG
            //System.out.println("DEBUG STATEMENT 8: NEW HIDDEN LAYER BIAS\n");
            //print(hiddenBias);

            // Update OUTPUT LAYER weights
            update(weightsHiddenOutput,sumOutputWeightGradient);

            // DEBUG
            //System.out.println("DEBUG STATEMENT 9: NEW OUTPUT LAYER WEIGHTS\n");
            //print(weightsHiddenOutput);

            // Update OUTPUT LAYER bias
            update(outputBias,sumOutputBiasGradient);

            // DEBUG
            //System.out.println("DEBUG STATEMENT 10: NEW OUTPUT LAYER bias\n");
            //print(outputBias);

            // ZERO OUT SUMMATIONS
            zero(sumHiddenWeightGradient);
            zero(sumHiddenBiasGradient);
            zero(sumOutputWeightGradient);
            zero(sumOutputBiasGradient);
        }

    }

    // Function takes in a double, z
    // Computes the sigmoid activation
    // Returns a double
    static double sigmoid(double z)
    {
        double activation = 1/(1+Math.exp(-z));
        return activation;
    }

    // Function takes in a double, a
    // Computes the derivative of sigmoid activation
    // Returns a double
    static double sigmoidDeriv(double a)
    {
        double derivative = a * (1-a);
        return derivative;
    }

    // Function takes in current matrix and the corresponding weight gradient
    // Updates the weights for that level
    // Returns nothing
    static void update(double[][] matrix, double[][] gradient) {
        for (int i = 0; i < matrix.length; i++) {
            for (int j = 0; j < matrix[i].length; j++) {

                // Update weights
                matrix[i][j] = matrix[i][j] - ((LEARNING_RATE * gradient[i][j]) / BATCH_SIZE);
            }
        }
    }

    // Functions takes in an int, label
    // Creates a corresponding one hot vector for the label
    // Returns the int[], one hot vector
    static int[] oneHot(int label)
    {
        int[] oneHot = new int[10];
        oneHot[label] = 1;
        return oneHot;
    }


    // Function takes in a path (.csv file), and a storage point (matrix)
    // Function stores the data from the file into the appropriate matrix
    // Returns nothing
    static void readData(String path, double[][] inputs, int[][] targets)
    {
        // Try to open the file
        try{
            Scanner dataReader = new Scanner(new File(path));
                // Keep track of list index
                int i = 0;
                // Try to read the file line by line
                while(dataReader.hasNextLine() && i < inputs.length)
                {
                    // Grab the line contents
                    String line = dataReader.next();


                    // Split the line into an array of items
                    String[] lineItems = line.split(",");

                    // The first item in list is the label
                    //      , so create a one hot vector and store in targets
                    targets[i] = oneHot(Integer.parseInt(lineItems[0]));

                    // Store the rest of the line as the input
                    for(int j = 0, k = 1; j < inputs[0].length;j++,k++)
                    {
                        inputs[i][j] = (double)Integer.parseInt(lineItems[k])/255;
                    }
                     i += 1;
                }

        }catch(FileNotFoundException e) {System.out.println("FILE NOT FOUND");}
    }

    // Function takes in a matrix
    // Fills the matrix w/ random numbers between (-1,1) inclusive
    // Returns nothing
    static double[][] randomize(double[][] A)
    {
        Random rand = new Random();
        for(int i = 0; i < A.length;i++)
        {
            for(int j = 0; j < A[i].length;j++)
            {
                A[i][j] = (rand.nextDouble() * 2) - 1;
            }
        }
        return A;
    }


    // Function takes in an (int) matrix
    // Finds the max item in the list
    // Returns the index of that item
    static int check(int[][] A)
    {
        // Set max as the first element
        int maxItem = A[0][0];
        // Variable will return the position of max element in the array
        int index = 0;
        for(int i = 0; i < A.length; i++)
        {
            for(int j = 0; j < A[0].length;j++)
            {
                if(A[i][j] > maxItem)
                {
                    maxItem = A[i][j];
                    index = i;
                }
            }

        }
        return index;
    }

    // Function takes in an (int) matrix
    // Finds the max item in the list
    // Returns the index of that item
    static int check2(double[][] A)
    {
        // Set max as the first element
        double maxItem = A[0][0];
        // Variable will return the position of max element in the array
        int index = 0;
        for(int i = 0; i < A.length; i++)
        {
            for(int j = 0; j < A[0].length;j++)
            {
                if(A[i][j] > maxItem)
                {
                    maxItem = A[i][j];
                    index = i;
                }
            }

        }
        return index;
    }

    // Function is used to randomize the mini batches
    // Generates a list of random indices between (0-60,000)
    // Returns that list
    static int[] scramble(int range)
    {
        Random rand = new Random();
        int[] miniIndices = new int[range];
        for(int i = 0; i < miniIndices.length;i++)
        {
            miniIndices[i] = rand.nextInt(range);
        }
        return miniIndices;
    }

    // Function saves the network state
    // Saves the weights & biases for HIDDEN LAYER and OUTPUT LAYER
    //      to a file w/ path "data/NetworkState.txt"
    // File Format:
    //      <Hidden Weights> (15 lines)
    //      <Hidden Bias> (15 lines)
    //      <Output Weights> (10 lines)
    //      <Output Bias> (10 lines)
    static void saveNetwork()
    {
        System.out.println("\nSaving Network...\n");
        try {

            // Open the file
            FileWriter fw = new FileWriter("data/NetworkState.txt");
            BufferedWriter bw = new BufferedWriter(fw);

            // Save the HIDDEN LAYER weights
            for (int i = 0; i < weightsInputHidden.length; i++) {
                String s = Arrays.toString(weightsInputHidden[i]).replace("[","").replace("]","");
                bw.write(s);
                bw.newLine();
            }


            // SAVE HIDDEN LAYER bias
            for (int i = 0; i < hiddenBias.length; i++) {
                String s = Arrays.toString(hiddenBias[i]).replace("[","").replace("]","");
                bw.write(s);
                bw.newLine();
            }

            // Save OUTPUT LAYER weights
            for (int i = 0; i < weightsHiddenOutput.length; i++) {
                String s = Arrays.toString(weightsHiddenOutput[i]).replace("[","").replace("]","");
                bw.write(s);
                bw.newLine();
            }

            // Save OUTPUT LAYER bias
            for (int i = 0; i < outputBias.length; i++) {
                String s = Arrays.toString(outputBias[i]).replace("[","").replace("]","");
                bw.write(s);
                bw.newLine();
            }

            bw.flush();

            System.out.println("SUCCESS: Network saved");
        }catch(Exception e){System.out.println("COULD NOT SAVE NETWORK");}

    }

    // Function retrieves a saved network state
    // Searches for a file w/ path "data/NetworkState.txt"
    // Opens that file, and restores the weights & biases
    //      for HIDDEN LAYER and OUTPUT LAYER
    // File Format:
    //      <Hidden Weights> (15 lines)
    //      <Hidden Bias> (15 lines)
    //      <Output Weights> (10 lines)
    //      <Output Bias> (10 lines)
    static void loadNetwork()
    {
        System.out.println("\nLoading Network...\n");
        try
        {
            // Open the file
            Scanner dataReader = new Scanner(new File("data/NetworkState.txt"));

            // Load the network from the file line by line
            while(dataReader.hasNextLine())
            {
                // Load the HIDDEN LAYER weights
                for(int i = 0; i < weightsInputHidden.length;i++)
                {
                    // Grab contents of single line
                    String line = dataReader.nextLine();
                    String[] lineItems = line.split(",");

                    // Convert each line item to a double, then store
                    for(int j = 0; j < weightsInputHidden[i].length;j++)
                    {
                        weightsInputHidden[i][j] = Double.parseDouble(lineItems[j]);
                    }
                }

                // Load HIDDEN LAYER bias
                for(int i = 0; i < hiddenBias.length;i++)
                {
                    // Grab contents of single line
                    String line = dataReader.nextLine();
                    String[] lineItems = line.split(",");

                    // Convert each line item to a double, then store
                    for(int j = 0; j < hiddenBias[i].length;j++)
                    {
                        hiddenBias[i][j] = Double.parseDouble(lineItems[j]);
                    }
                }

                // Load OUTPUT LAYER weights
                for(int i = 0; i < weightsHiddenOutput.length;i++)
                {
                    // Grab contents of single line
                    String line = dataReader.nextLine();
                    String[] lineItems = line.split(",");

                    // Convert each line item to a double, then store
                    for(int j = 0; j < weightsHiddenOutput[i].length;j++)
                    {
                        weightsHiddenOutput[i][j] = Double.parseDouble(lineItems[j]);
                    }
                }

                // Load OUTPUT LAYER biases
                for(int i = 0; i < outputBias.length;i++)
                {
                    // Grab contents of single line
                    String line = dataReader.nextLine();
                    String[] lineItems = line.split(",");

                    // Convert each line item to a double, then store
                    for(int j = 0; j < outputBias[i].length;j++)
                    {
                        outputBias[i][j] = Double.parseDouble(lineItems[j]);
                    }
                }
            }

            System.out.println("SUCCESS: Network loaded");

        }catch(Exception e){System.out.println("Could not find data/NetworkState.txt");}
    }
    //endregion



    //region ************** MATRIX UTILITY *****************
    // Function takes in a matrix A
    // Grabs the specified column
    // Returns that column as a 1D array
    static double[] column(double[][] A, int column)
    {
        double[] B = new double[A.length];
        for(int i = 0; i < A.length; i++)
        {
            B[i] = A[i][column];
        }
        return B;
    }

    // Function takes in a 2D array, matrix
    // Turns the matrix into a 1D array
    // Returns the 1D array form
    static double[] transpose(double[][] matrix)
    {
        double[] newArr = new double[matrix.length];
        for(int i = 0; i < matrix.length; i++)
        {
            newArr[i] = matrix[i][0];
        }
        return newArr;
    }

    // Function takes in a 2D array, matrix
    // Turns the matrix into a 1D array
    // Returns the 1D array form
    static double[] transpose2(int[][] matrix)
    {
        double[] newArr = new double[matrix.length];
        for(int i = 0; i < matrix.length; i++)
        {
            newArr[i] = matrix[i][0];
        }
        return newArr;
    }

    // Function takes in a matrix (2D array)
    // Flushes the matrix (zeroes it out)
    // Returns nothing
    static void zero(double[][] matrix)
    {
        for(int i = 0; i < matrix.length; i++)
        {
            for(int j = 0; j < matrix[i].length; j++)
            {
                matrix[i][j] = 0.0;
            }
        }
    }

    // Function that takes in a 1D array
    // Returns a 2D array
    static int[][] convert(int[] A)
    {
        // Create a matrix w/ inverse dimensions
        int[][] B = new int[A.length][1];

        for(int i = 0; i < A.length; i++)
        {
            B[i][0] = A[i];
        }
        return B;
    }

    // Function that takes in a 1D array
    // Returns a 2D array
    static double[][] convert2(double[] A)
    {
        // Create a matrix w/ inverse dimensions
        double[][] B = new double[A.length][1];

        for(int i = 0; i < A.length; i++)
        {
            B[i][0] = A[i];
        }
        return B;
    }

    static void reset(int[] A)
    {
        for(int i = 0; i < A.length; i++)
        {
            A[i] = 0;
        }
    }



    //endregion




    //region ************** OUTPUT GENERATION ***************
    static void print(double[][] A)
    {
        for(int i = 0; i < A.length;i++)
        {
            System.out.println(Arrays.toString(A[i]));
        }
        System.out.println("\n");
    }

    // Functions takes in a matrix and prints it
    static void print2(int[][] matrix)
    {
        for(int i = 0; i < matrix.length; i++)
        {
            System.out.println(Arrays.toString(matrix[i]));
        }
    }

    // Function displays NETWORK ACCURACY
    static void showAccuracy()
    {
        for(int i = 0; i < 10;i++)
        {
            if(i == 6)
            {
                System.out.println("\n");
            }
            String s = String.format("%d = %d / %d  ",i, digitCorrect[i], digitTotal[i]);
            System.out.print(s);
        }
        String p = String.format("Accuracy = %d / %d = %f", correct, total, ((double)correct/(double)total)*100);
        System.out.print(p + "%\n");
    }

    // Function takes in a 1D array containing pixel stream
    // Turns the pixel stream back into an image
    // Returns the image
    static double[][] pixelate(double[] input)
    {
        // Stores the digitized input
        double[][] pixel = new double[28][28];

        // Tracks index of regular input
        int index = 0;

        for(int  i = 0; i < pixel.length;i++)
        {
            for(int j = 0; j < pixel[i].length;j++)
            {
                pixel[i][j] = input[index];
                index += 1;
            }
        }
        return pixel;
    }
    
    static void printImage(double[][] image)
    {
        for(int i = 0; i < image.length; i++)
        {
            String line = "";
            for(int j = 0; j < image[i].length;j++)
            {
                char asciiChar = (image[i][j] == 0) ? ' ' : '*';
                line += asciiChar;
            }
            System.out.println(line);

        }

    }

    //endregion
}
