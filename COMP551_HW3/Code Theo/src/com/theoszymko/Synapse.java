package com.theoszymko;

public class Synapse {
	private Neuron neuronSource;
	private double weight;
	
	public Synapse(Neuron source, double weight) {
		this.neuronSource = source;
		this.weight = weight;
	}

	public double getWeight() {
		return weight;
	}

	public void setWeight(double weight) {
		this.weight = weight;
	}
	
	public Neuron getSource() {
		return this.neuronSource;
	}
}
