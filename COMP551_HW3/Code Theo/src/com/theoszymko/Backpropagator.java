package com.theoszymko;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;

import com.theoszymko.training.DataSet;
import com.theoszymko.training.TrainingDataGenerator;

public class Backpropagator {
	private double learningRate;
	private NeuralNet neuralNet;
	private double momentum;
	private double characteristicTime;
	private int epoch;
	private double dropOut;
	
	/**
	 * Backpropagates with respect to some inputs and output
	 * on a neural network
	 * 
	 * @param neuralNet - the actual neural network
	 * @param learningRate - learning rate of the neural network
	 */
	public Backpropagator(NeuralNet neuralNet, double learningRate, double momentum, double characteristicTime, double dropOut) {
		this.learningRate = learningRate;
		this.neuralNet = neuralNet;
		this.momentum = momentum;
		this.characteristicTime = characteristicTime;
		this.dropOut = dropOut;
	}
	
	/**
	 * Train the net with backpropagation using an error threshold.
	 * The net will continue backpropagating until the error is below
	 * the threshold
	 * 
	 * @param inputs
	 * @param outputs
	 * @param errorThreshold
	 */
	 public void train(TrainingDataGenerator generator, double errorThreshold, double maxEpoch) {
	        double error;
	        double sum = 0.0;
	        double average = 25;
	        epoch = 1;
	        int samples = 25;
	        double[] errors = new double[samples];

	        do {
	            DataSet trainingData = generator.getDataSet();
	            error = backpropagate(trainingData.inputs, trainingData.outputs);

	            sum -= errors[epoch % samples];
	            errors[epoch % samples] = error;
	            sum += errors[epoch % samples];

	            if(epoch > samples) {
	                average = sum / samples;
	            }
	            
	            System.out.println("Error for epoch " + epoch + ": " + error + ". Average: " + average +" Learning rate: " + learningRate);
	            epoch++;
	        } while(average > errorThreshold && epoch < maxEpoch);
	}
	
	/**
	 * Backpropagate error onto the neural network
	 * and performs an update of all the weights
	 * 
	 * @param inputs - an array of array of inputs
	 * @param outputs - an array of array of outputs
	 */
	public double backpropagate(double[][] inputs, double[][] outputs) {
		double error = 0.0d;
		double wrongGuesses = 0.0d;
		
		HashMap<Synapse, Double> snypaseDetla = new HashMap<Synapse, Double>();
		
		for(int i = 0; i < inputs.length; i++) {
			// For each training example
			double[] input = inputs[i];
			double[] expectedOutput = outputs[i];
			
			// Extract value from one-hot vector
			double expectedSingleOutput = 0;
			for(int k = 0; k < expectedOutput.length; k++) {
				if(expectedOutput[k] == 1) { expectedSingleOutput = k; } 
			}
			
			// We compute the output of the neural net for this input
			List<Layer> layers = this.neuralNet.getLayers();
			this.neuralNet.setInputs(input);
			double[] output = this.neuralNet.getOutput();
			
			// First step is to compute the error and back-propagate it
			// all the way to the input layer
			// For each layer starting by the output layer
			for(int j = layers.size()-1; j > 0; j--) {
				Layer layer = layers.get(j);
				List<Neuron> neurons = layer.getNeurons();
				
				// For each neuron of this layer
				for(int k = 0; k < neurons.size(); k++) {
					Neuron neuron = neurons.get(k);
					double gradient = 0.0d;
					
					if(layer.isOutputLayer()) {
						// Determine the gradient of the neuron
						gradient = neuron.getDerivative() * (output[k] - expectedOutput[k]); // -> determine the sign of the gradient
					} else {
						gradient = neuron.getDerivative();
						
						double sum = 0.0d;
						// We sum over the downstream neurons to get 
						// the gradient
						for(Neuron downNeuron : layer.getNextLayer().getNeurons()) {
							// Check if the downstream neuron is connected to this neuron
							for(Synapse synapse : downNeuron.getInputs()) {
								if(synapse.getSource() == neuron) {
									sum += (synapse.getWeight() * downNeuron.getError());
									break;
								}
							}
						}
						
						gradient *= sum;
					}
					
					// Dropout
					if(Math.random() > (1-dropOut)) {
						// Cripple the gradient
						gradient = 0;
					}
					
					neuron.setError(gradient);
				}
			}
			
			// Second step, we use the pre-computed gradient to update
			// the weights of the network
			// For each layer starting by the output layer
			for(int j = layers.size()-1; j > 0; j--) {
				Layer layer = layers.get(j);
				ArrayList<Neuron> neurons = (ArrayList<Neuron>) layer.getNeurons();
							
				// For each neuron of this layer
				for(int k = 0; k < neurons.size(); k++) {
					Neuron neuron = neurons.get(k);
					
					for(Synapse synapse : neuron.getInputs()) {
						// Compute the delta
						double newLearningRate = this.characteristicTime > 0 ? (this.learningRate / (epoch / this.characteristicTime)) : this.learningRate;
						double delta = newLearningRate * neuron.getError() * synapse.getSource().getOutput();
						
						if(snypaseDetla.get(synapse) != null) {
							delta += snypaseDetla.get(synapse) * this.momentum;
						}
						
						// Update weight
						snypaseDetla.put(synapse, delta);
						synapse.setWeight(synapse.getWeight() - delta);
					}
				}
			}
			
			output = this.neuralNet.getOutput();
	        error += error(output, expectedOutput);
	        
	        // Extract value from one-hot vector
	        double singleOutput = 0;
	        double max = 0;
	     	for(int k = 0; k < output.length; k++) {
	     		if(output[k] > max) { max = output[k]; singleOutput = k; } 
	     	}
	     			
	        if(singleOutput != expectedSingleOutput) {
	        	wrongGuesses++;
	        }
		}
		
		return error;
	}
	
	public double error(double[] actual, double[] expected) {

        if (actual.length != expected.length) {
            throw new IllegalArgumentException("The lengths of the actual and expected value arrays must be equal");
        }

        double sum = 0;

        for (int i = 0; i < expected.length; i++) {
            sum += Math.pow(expected[i] - actual[i], 2);
        }

        return sum / 2;
    }
}
