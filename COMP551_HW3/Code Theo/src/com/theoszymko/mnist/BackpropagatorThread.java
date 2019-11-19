package com.theoszymko.mnist;

import com.theoszymko.Backpropagator;
import com.theoszymko.NeuralNet;
import com.theoszymko.training.TrainingDataGenerator;

public class BackpropagatorThread implements Runnable {
	private double learningRate, momentum;
	private NeuralNet neuralNet;
	private TrainingDataGenerator generator;
	
	public BackpropagatorThread(NeuralNet neuralNet, double learningRate, double momentum, TrainingDataGenerator generator) {
		this.learningRate = learningRate;
		this.neuralNet = neuralNet;
		this.momentum = momentum;
		this.generator = generator;
	}
	
	@Override
	public void run() {
		Backpropagator backprogagator = new Backpropagator(this.neuralNet, this.learningRate, this.momentum, 0, 0);
		backprogagator.train(this.generator, 0.005, 100000);
	}
}
