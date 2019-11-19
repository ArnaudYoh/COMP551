package com.theoszymko;

import java.util.ArrayList;

public class Neuron {
	/**
	 * Activation method used
	 * to compute the activation
	 * of the the neuron
	 */
	private ActivationFunction activationFn;
	
	/**
	 * List of neurons for which their output
	 * is connected to the input of this neuron
	 */
	private ArrayList<Synapse> inputs;
	
	/**
	 * Output of the neuron
	 */
	private double output;
	
	/**
	 * Derivative of the output
	 * of the neuron
	 */
	private double derivative;
	
	/**
	 * Sum of all the weight
	 * of the synapses connected to this
	 * neuron
	 */
	private double preActivation;
	
	/**
	 * Used for backpropagation
	 */
	private double error;
	
	// For test purposes
	public String name;

	public Neuron(ActivationFunction fn) {
		this.activationFn = fn;
		
		this.inputs = new ArrayList<Synapse>();
		this.error = 0;
	}
	
	/**
	 * Connect a new neuron to the input of this
	 * neuron throught a synapse
	 * @param input - synapse
	 */
	public void addInput(Synapse input) {
		this.inputs.add(input);
	}
	
	/**
	 * Return the weight matrix
	 * which is computed from the weight
	 * of each synapse
	 * @return the weight matrix for this neuron
	 */
	public double[] getWeights() {
		double[] weights = new double[this.inputs.size()];
		
		int i = 0;
		for(Synapse synapse : this.inputs) {
			weights[i] =  synapse.getWeight();
			i++;
		}
		
		return weights;
	}
	
	/**
	 * Computes the pre-activation value
	 * of this neuron
	 */
	public void computePreActivation() {
		this.preActivation = 0;
		
		for(Synapse synapse : this.inputs) {
			this.preActivation += synapse.getWeight() * synapse.getSource().getOutput();
		}
		
	}
	
	/**
	 * Compute the 
	 */
	public void activate() {
		this.computePreActivation();
		
		this.output = this.activationFn.activate(this.preActivation);
		this.derivative = this.activationFn.derivative(this.output);
	}
	
	/**
	 * Return the output of the neuron
	 * @return output
	 */
	public double getOutput() {
		return output;
	}
	
	public void setOutput(double output) {
        this.output = output;
    }
	
	public double getDerivative() {
        return this.derivative;
    }
	
	public ArrayList<Synapse> getInputs() {
		return this.inputs;
	}

	public double getError() {
		return error;
	}

	public void setError(double error) {
		this.error = error;
	}
}
