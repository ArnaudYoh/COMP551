package com.theoszymko;

import java.util.ArrayList;

public class Layer {
	private ArrayList<Neuron> neurons;
	private Layer previousLayer;
	private Layer nextLayer;
	
	private Neuron bias;
	
	/**
	 * Init empty layer
	 */
	public Layer() {
		this.neurons = new ArrayList<Neuron>();
		this.previousLayer = null;
	}
	
	/**
	 * Init a layer connected to previous
	 * layer
	 * @param previousLayer
	 */
	public Layer(Layer previousLayer) {
		this();
		this.previousLayer = previousLayer;
	}
	
	/**
	 * Input a layer connected to previous layer
	 * and with a bias
	 * 
	 * @param previousLayer
	 * @param bias
	 */
	public Layer(Layer previousLayer, Neuron bias) {
		this(previousLayer);
		this.bias = bias;
		
		this.neurons.add(bias);
	}
	
	/**
	 * Add a neuron to the layer
	 * All weights are initialized randomly between 0 and 1
	 * @param neuron
	 */
	public void addNeuron(Neuron neuron) {
		this.neurons.add(neuron);
		
		// Connect this new neuron to the previous layer
		if(this.previousLayer != null) {
			for(Neuron previousNeuron : this.previousLayer.getNeurons()) {
				// Add a synapse to previous neuron
				neuron.addInput(new Synapse(previousNeuron, (Math.random() * 1) - 0.5));
			}
		}
	}
	
	/**
	 * Add a neuron to the layer
	 * Must provide the weight for each of the neuron
	 * 
	 * @param neuron
	 * @param weights
	 */
	public void addNeuron(Neuron neuron, double weights[]) {
		this.neurons.add(neuron);
		
		// Connect this new neuron to the previous layer
		if(this.previousLayer != null) {
			if(this.previousLayer.getNeurons().size() != weights.length) {
				throw new IllegalArgumentException("Weights must match the size of the previous layer");
			} else {
				// Good size
				int i = 0;
				for(Neuron previousNeuron : this.previousLayer.getNeurons()) {
					// Add a synapse to previous neuron
					neuron.addInput(new Synapse(previousNeuron, weights[i]));
					i++;
				}
			}
		}
	}
	
	/**
	 * Activate the layer based on the previous layer
	 * (no argument needed because connections are done 
	 * trought the synapses)
	 */
	public void feedForward() {
		for(int i = (this.hasBias() ? 1 : 0); i < this.neurons.size(); i++) {
			this.neurons.get(i).activate();
		}
	}
	
	public ArrayList<Neuron> getNeurons() {
		return this.neurons;
	}
	
	public Layer getPreviousLayer() {
        return previousLayer;
    }

	/**
	 * You can only assign a previous layer
	 * before adding neurons
	 * @param previousLayer
	 */
    void setPreviousLayer(Layer previousLayer) {
        this.previousLayer = previousLayer;
    }
    
    public Layer getNextLayer() {
        return nextLayer;
    }

    void setNextLayer(Layer nextLayer) {
        this.nextLayer = nextLayer;
    }
    
    public boolean isOutputLayer() {
        return nextLayer == null;
    }

    public boolean hasBias() {
        return bias != null;
    }
}
