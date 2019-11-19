package com.theoszymko.mnist;

import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashMap;
import java.util.LinkedHashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;

import com.theoszymko.Backpropagator;
import com.theoszymko.Layer;
import com.theoszymko.LinearActivationFunction;
import com.theoszymko.NeuralNet;
import com.theoszymko.Neuron;
import com.theoszymko.SigmoidActivationFunction;
import com.theoszymko.Synapse;
import com.theoszymko.training.DataSet;
import com.theoszymko.training.TrainingDataGenerator;

public class Mnist {
	public static int[] layers;
	
	public static void main(String[] args) {
		// load arguments
		boolean loadWeights = true;
		layers = new int[]{718, 400, 50};
		int mnistTrainingSize = 20;
		double momentum = 0.4;
		double training = 0.2;
		int kaggleValidationSize = 5;
		int maxEpoch = 10000;
		double dropOut = 0.2;
		
		for(int i = 0; i < args.length; i++) {
			String command = args[i];
			
			if(command.equals("-train")) {
				loadWeights = false;
			}
			
			if(command.equals("-load")) {
				loadWeights = true;
			}
			
			if(command.equals("-traingSize")) {
				mnistTrainingSize = Integer.valueOf(args[i+1]);
				i++;
			}
			
			if(command.equals("-kaggleSize")) {
				kaggleValidationSize = Integer.valueOf(args[i+1]);
				i++;
			}
			
			if(command.equals("-maxEpoch")) {
				maxEpoch = Integer.valueOf(args[i+1]);
				i++;
			}
			
			if(command.equals("-dropout")) {
				dropOut = Double.valueOf(args[i+1]);
				i++;
			}
			
			if(command.equals("-layers")) {
				ArrayList<Integer> layersDef = new ArrayList<Integer>();
				try {
					int k = 1;
					while(true) {
						layersDef.add(Integer.valueOf(args[i+k]));
						k++;
					}
				} catch(Exception e) {
				}
				
				layers = new int[layersDef.size()];
				int j = 0;
				for(int k : layersDef) {
					layers[j] = k;
					j++;
				}
			}
		}
		
		// Create the neural net
		NeuralNet mnistNeuralNet = createMnistNeuralNet();
		
		// Reading data
		if(!loadWeights && mnistTrainingSize > 0) {
			TrainingDataGenerator mnistTrainingData = new MnistTrainingDataGenerator(mnistTrainingSize);

			Backpropagator backprogagator = new Backpropagator(mnistNeuralNet, training, momentum, 0, dropOut);
			backprogagator.train(mnistTrainingData, 0.005, maxEpoch);

			saveWeights(mnistNeuralNet);
		} else {
			restoreFromWeights(mnistNeuralNet);
		}
		
		// Test Data accuracy
		TrainingDataGenerator mnistTestData = new MnistValidationDataGenerator(1000);
		double accuracy = accuracy(mnistTestData, mnistNeuralNet);
		
		System.out.println("Accuracy is "+accuracy+"% on validation set");
		
		// Prof's data
		if(kaggleValidationSize != 0) {
			KaggleTrainingDataGenerator kaggle = new KaggleTrainingDataGenerator(kaggleValidationSize);
			accuracy = doPatchScan(kaggle.getDataSet(), mnistNeuralNet);
	
			System.out.println("Accuracy is "+accuracy+"% on prof's set");
		}
	}
	
	public static double doPatchScan(DataSet dataset, NeuralNet net) {
		double[][] inputs = dataset.inputs;
		double[][] outputs= dataset.outputs;
		double dataSize = dataset.inputs.length;
		double rightGuesses = 0;
		
		for(int i = 0; i < inputs.length; i++) {
			double[] input = inputs[i];
			double expectedOutput = outputs[i][0];
			
			ArrayList<Integer> founds = new ArrayList<Integer>();
			HashMap<Integer, Double> foundsWithAccuracy = new HashMap<Integer, Double>();
			
			double[] foundsSumConfidence = new double[10];
			double[] numberOfTimesFound = new double[10];
			
			for(int x = 0; x < 32; x += 3) {
				for(int y = 0; y < 32; y += 3) {
					double[] patch = getPatchAt(x, y, input);
					
					net.setInputs(patch);
					double[] netOutput = net.getOutput();
					double max = 0;
					int guessed = -1;
					
					for(int k = 0; k < netOutput.length; k++) {
						if(netOutput[k] > max) {
							max = netOutput[k];
							guessed = k;
							
							//System.out.println("Guessed "+k+" (confience: "+netOutput[k]+")");
						}
					}

					if(max > 0.9 && !founds.contains(guessed)) {
						founds.add(guessed);
					}
					
					foundsSumConfidence[guessed] += max;
					numberOfTimesFound[guessed]++;
					
					if(foundsWithAccuracy.containsKey(guessed)) {
						double previousAcc = foundsWithAccuracy.get(guessed);
						if(max > previousAcc) {
							foundsWithAccuracy.put(guessed, max);
						}
					} else {
						foundsWithAccuracy.put(guessed, max);
					}
				}
			}
			
			int numberA = -1;
			int numberB = -1;
			
			Map<Integer, Double> sorted = sortByValue(foundsWithAccuracy);
			for(Integer a : sorted.keySet()) {
				System.out.println("Found "+a+" with accuracy "+foundsWithAccuracy.get(a)+" average="+(foundsSumConfidence[a]/numberOfTimesFound[a])+" found="+numberOfTimesFound[a]);
				
				if(numberA == -1) {
					numberA = a;
				} else if(numberB == -1) {
					numberB = a;
				} else {
					//break;
				}
			}
			
			if(numberB == -1) {
				numberB = numberA;
			}
			double output = numberA + numberB;
			
			//for(Integer a : founds) { System.out.println(a); }
			//System.out.println("A: "+numberA+" ("+numberAx+","+numberAy+"), B: "+numberB+" ("+numberBx+","+numberBy+")");
			
			if(output == expectedOutput) {
				rightGuesses++;
			}
			
			System.out.println("Guessed "+output+" ("+numberA+" + "+numberB+"), was "+expectedOutput);
		}
		
		return (rightGuesses/dataSize) * 100.0d;
	}
	
	// Extract a patch from the image
	public static double[] getPatchAt(int x, int y, double[] input) {
		double[] patch = new double[28 * 28];
		int length = input.length;
		int lineSize = 60;
		
		for(int i = y; i < y+28; i += 1) {
			int lineStart = lineSize * i;
			
			for(int k = x; k < x+28; k += 1) {
				int patchIndex = (i-y)*28 + (k-x);
				int inputIndex = lineStart + k;
				//System.out.println("Patch="+patchIndex+", input="+inputIndex);
				patch[patchIndex] = input[inputIndex]; 
			}
		}
		
		return patch;
	}
	
	public static double accuracy(TrainingDataGenerator validationSet, NeuralNet net) {
		DataSet data = validationSet.getDataSet();
		
		double dataSize = data.inputs.length;
		double rightGuesses = 0;
		
		for(int i = 0; i < data.inputs.length; i++) {
			double[] input = data.inputs[i];
			double[] expectedOutput = data.outputs[i];
			double expectedOutputSignle = 0;
			
			// Extract value from one-hot vector
			for(int k = 0; k < expectedOutput.length; k++) {
				if(expectedOutput[k] != 0) { expectedOutputSignle = k; }
			}
			
			net.setInputs(input);
			double[] output = net.getOutput();
		
			double guess = 0;
			double max = 0;
			
			// Extract value from output
			for(int k = 0; k < output.length; k++) {
				if(output[k] > max) {
					max = output[k];
					guess = k;
				}
			}
			
			rightGuesses += (guess == expectedOutputSignle ? 1 : 0);
		}
		
		return (rightGuesses/dataSize) * 100.0d;
	}
	
	public static NeuralNet createMnistNeuralNet() {
		NeuralNet net = new NeuralNet();
		
		// Creating input layer
		Neuron inputBias = new Neuron(new SigmoidActivationFunction());
		inputBias.setOutput(1);
		
		Layer inputLayer = new Layer(null, inputBias);
		int inputSize = 28*28;
		
		for(int i = 0; i < inputSize; i++) {
			Neuron n = new Neuron(new SigmoidActivationFunction());
			inputLayer.addNeuron(n);
		}
		
		// First hidden layer
		int[] layersSizes = layers;
		Layer lastLayer = null;
		ArrayList<Layer> hiddenLayers = new ArrayList<Layer>();
		
		for(int i = 0; i < layersSizes.length; i++) {
			int neuronCount = layersSizes[i];
			
			// Creating layer
			Layer layer;
			Neuron bias = new Neuron(new SigmoidActivationFunction());
			bias.setOutput(0);
			
			if(lastLayer == null) {
				layer = new Layer(inputLayer, bias);
			} else {
				layer = new Layer(lastLayer, bias);
			}
			
			for(int k = 0; k < neuronCount; k++) {
				Neuron n = new Neuron(new SigmoidActivationFunction());
				n.setOutput(0);
				layer.addNeuron(n);
			}
			
			// Save layer
			hiddenLayers.add(layer);
			lastLayer = layer;
		}
		
		// Output layer
		Layer outputlayer = new Layer(lastLayer);
		int outputSize = 10;
		
		for(int i = 0; i < outputSize; i++) {
			Neuron n = new Neuron(new SigmoidActivationFunction());
			outputlayer.addNeuron(n);
		}
		
		// Adding layer to neural net
		net.addLayer(inputLayer);
		for(Layer layer : hiddenLayers) {
			net.addLayer(layer);
		}
		net.addLayer(outputlayer);
		
		// Net is good !
		return net;
	}
	
	public static void saveWeights(NeuralNet net) {
		String name = "neural-net";
		
		for(Layer layer : net.getLayers()) {
			name += "-"+layer.getNeurons().size();
		}
		
		name += ".weights";
		
		try{
		    PrintWriter writer = new PrintWriter(name, "UTF-8");
		    
		    int l = 0;
		    int count = 0;

		    for(Layer layer : net.getLayers()) {
		    	// Do not save input layer
		    	if(l == 0) {
		    		l++;
		    		continue;
		    	}
		    	
		    	for(Neuron neuron : layer.getNeurons()) {
		    		for(Synapse synapse : neuron.getInputs()) {
		    			count++;
		    		}
		    	}
		    	
		    	l++;
		    }
		    
		    int i = 0;
		    writer.println(count+",");
		    for(Layer layer : net.getLayers()) {
		    	// Do not save input layer
		    	if(i == 0) {
		    		i++;
		    		continue;
		    	}
		    	
		    	for(Neuron neuron : layer.getNeurons()) {
		    		for(Synapse synapse : neuron.getInputs()) {
		    			writer.println(synapse.getWeight()+",");
		    		}
		    	}
		    	
		    	i++;
		    }
		    writer.flush();
		    
		    writer.close();
		} catch (Exception e) {
		   // do something
		}
	}
	
	public static void restoreFromWeights(NeuralNet net) {
		String name = "neural-net";
		
		for(Layer layer : net.getLayers()) {
			name += "-"+layer.getNeurons().size();
		}
		
		name += ".weights";
		
        BufferedReader br = null;
        String line = "";
        String cvsSplitBy = ",";

        try {

            br = new BufferedReader(new FileReader(name));
            int count = 0;
            
            int i = 0;
            br.readLine();
		    for(Layer layer : net.getLayers()) {
		    	// Do not save input layer
		    	if(i == 0) {
		    		i++;
		    		continue;
		    	}
		    	
		    	for(Neuron neuron : layer.getNeurons()) {
		    		for(Synapse synapse : neuron.getInputs()) {
		    			line = br.readLine();
		    			line = line.replace(",", "");
		    			double weight = Double.valueOf(line);
		    			synapse.setWeight(weight);
		    		}
		    	}
		    	
		    	i++;
		    }

        } catch (FileNotFoundException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            if (br != null) {
                try {
                    br.close();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }
	}
	
	// from http://stackoverflow.com/questions/109383/sort-a-mapkey-value-by-values-java
	public static <K, V extends Comparable<? super V>> Map<K, V> sortByValue( Map<K, V> map )
	{
	    List<Map.Entry<K, V>> list =
	        new LinkedList<>( map.entrySet() );
	    Collections.sort( list, new Comparator<Map.Entry<K, V>>()
	    {
	        @Override
	        public int compare( Map.Entry<K, V> o1, Map.Entry<K, V> o2 )
	        {
	            return ( o2.getValue() ).compareTo( o1.getValue() );
	        }
	    } );
	
	    Map<K, V> result = new LinkedHashMap<>();
	    for (Map.Entry<K, V> entry : list)
	    {
	        result.put( entry.getKey(), entry.getValue() );
	    }
	    return result;
	}
}
