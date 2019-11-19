package com.theoszymko;

import com.theoszymko.training.XorTrainingDataGenerator;

public class Main {
	public static void main(String[] args) {
		NeuralNet untrained = createUntrainedXorNeuralNetwork();

        Backpropagator backpropagator = new Backpropagator(untrained, 0.1, 0.9, 0, 0);        
        backpropagator.train(new XorTrainingDataGenerator(), 0.0001, 100);

        System.out.println("Testing trained XOR neural network");

        untrained.setInputs(new double[]{0, 0});
        System.out.println("0 XOR 0: " + (untrained.getOutput()[0]));

        untrained.setInputs(new double[]{0, 1});
        System.out.println("0 XOR 1: " + (untrained.getOutput()[0]));

        untrained.setInputs(new double[]{1, 0});
        System.out.println("1 XOR 0: " + (untrained.getOutput()[0]));

        untrained.setInputs(new double[]{1, 1});
        System.out.println("1 XOR 1: " + (untrained.getOutput()[0]) + "\n");
	}
	
	public static void testAndNeuralNet() {
		System.out.println("Testing AND function");
		NeuralNet andNeuralNetwork = new NeuralNet();
		
		Layer inputLayer = new Layer(null);
		
		Neuron a = new Neuron(new ThresoldActivationFunction(1));
        Neuron b = new Neuron(new ThresoldActivationFunction(1));

        inputLayer.addNeuron(a);
        inputLayer.addNeuron(b);
		
		Layer outputLayer = new Layer(inputLayer);
		Neuron andNeuron = new Neuron(new ThresoldActivationFunction(1.5));
        outputLayer.addNeuron(andNeuron, new double[]{1, 1});
		
		andNeuralNetwork.addLayer(inputLayer);
		andNeuralNetwork.addLayer(outputLayer);
        
		andNeuralNetwork.setInputs(new double[]{0, 0});
        System.out.println("0 AND 0: " + andNeuralNetwork.getOutput()[0]);

        andNeuralNetwork.setInputs(new double[]{0, 1});
        System.out.println("0 AND 1: " + andNeuralNetwork.getOutput()[0]);

        andNeuralNetwork.setInputs(new double[]{1, 0});
        System.out.println("1 AND 0: " + andNeuralNetwork.getOutput()[0]);
        
        andNeuralNetwork.setInputs(new double[]{1, 1});
        System.out.println("1 AND 1: " + andNeuralNetwork.getOutput()[0] + "\n");
	}
	
	private static NeuralNet createUntrainedXorNeuralNetwork() {
		NeuralNet xorNeuralNetwork = new NeuralNet();

        Neuron inputBias = new Neuron(new SigmoidActivationFunction());
        inputBias.setOutput(1);
        Layer inputLayer = new Layer(null, inputBias);

        Neuron a = new Neuron(new SigmoidActivationFunction());
        a.setOutput(0);

        Neuron b = new Neuron(new SigmoidActivationFunction());
        b.setOutput(0);

        inputLayer.addNeuron(a);
        inputLayer.addNeuron(b);

        Neuron bias = new Neuron(new SigmoidActivationFunction());
        bias.setOutput(1);
        Layer hiddenLayer = new Layer(inputLayer, bias);

        Neuron hiddenA = new Neuron(new SigmoidActivationFunction());
        Neuron hiddenB = new Neuron(new SigmoidActivationFunction());

        hiddenLayer.addNeuron(hiddenA);
        hiddenLayer.addNeuron(hiddenB);

        Layer outputLayer = new Layer(hiddenLayer);
        Neuron xorNeuron = new Neuron(new SigmoidActivationFunction());
        outputLayer.addNeuron(xorNeuron);

        xorNeuralNetwork.addLayer(inputLayer);
        xorNeuralNetwork.addLayer(hiddenLayer);
        xorNeuralNetwork.addLayer(outputLayer);

        return xorNeuralNetwork;
    }
	
	private static NeuralNet createXorNeuralNetwork() {
		NeuralNet xorNeuralNetwork = new NeuralNet();

        Layer inputLayer = new Layer(null);

        Neuron a = new Neuron(new ThresoldActivationFunction(1));
        a.setOutput(0);

        Neuron b = new Neuron(new ThresoldActivationFunction(1));
        b.setOutput(0);

        inputLayer.addNeuron(a);
        inputLayer.addNeuron(b);

        Layer hiddenLayer = new Layer(inputLayer);

        Neuron hiddenA = new Neuron(new ThresoldActivationFunction(1.5));
        Neuron hiddenB = new Neuron(new ThresoldActivationFunction(0.5));

        hiddenLayer.addNeuron(hiddenA, new double[]{1, 1});
        hiddenLayer.addNeuron(hiddenB, new double[]{1, 1});

        Layer outputLayer = new Layer(hiddenLayer);
        Neuron xorNeuron = new Neuron(new ThresoldActivationFunction(0.5));
        outputLayer.addNeuron(xorNeuron, new double[]{-1, 1});

        xorNeuralNetwork.addLayer(inputLayer);
        xorNeuralNetwork.addLayer(hiddenLayer);
        xorNeuralNetwork.addLayer(outputLayer);

        return xorNeuralNetwork;
    }
}
