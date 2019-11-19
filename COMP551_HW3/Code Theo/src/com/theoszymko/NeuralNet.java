package com.theoszymko;

import java.util.ArrayList;

public class NeuralNet {
	private ArrayList<Layer> layers;
	private Layer input, output;
	
	public NeuralNet() {
		layers = new ArrayList<Layer>();
	}
	
	/**
	 * Add a layer at the end of the neural net
	 * this new layer will automatically become
	 * the output layer for the neural net
	 * @param layer - new layer
	 */
	public void addLayer(Layer layer) {
		this.layers.add(layer);
		
		if(this.layers.size() == 1) {
			this.input = layer;
		}
		
		if(this.layers.size() > 1) {
			Layer previousLayer = this.layers.get(this.layers.size() - 2);
			previousLayer.setNextLayer(layer);
		}
		
		this.output = this.layers.get(this.layers.size() - 1);
	}

	/**
	 * Reset the weight to random for all synapses
	 * of all neurons of all layers
	 * 
	 * Warning: O(n^3)
	 */
	public void reset() {
		for(Layer layer : this.layers) {
			for(Neuron neuron : layer.getNeurons()) {
				for(Synapse synapse : neuron.getInputs()) {
					synapse.setWeight((Math.random() * 1) - 0.5);
				}
			}
		}
	}
	
	/**
	 * Sets the output of the input layer
	 * @param inputs
	 */
	public void setInputs(double[] inputs) {
		if(this.input == null) {
			throw new RuntimeException("No input layer");
		}
		
		int layerSize = (input.hasBias() ? input.getNeurons().size() - 1 : input.getNeurons().size());
		
		if(layerSize != inputs.length) {
			throw new RuntimeException("Inputs must be of the same size as the layer");
		}
		
		int biasCount = input.hasBias() ? 1 : 0;
		for(int i = biasCount; i < input.getNeurons().size(); i++) {
			input.getNeurons().get(i).setOutput(inputs[i - biasCount]);
		}
	}
	
	/**
	 * Feed forward the inputs and
	 * returns the matrix output of the last
	 * layer
	 * @return
	 */
	public double[] getOutput() {
		if(this.output == null) {
			throw new RuntimeException("No output layer");
		}
		
		double[] outputs = new double[output.getNeurons().size()];
		
		for(int i = 1; i < layers.size(); i++) {
			layers.get(i).feedForward();
		}
		
		int i = 0;
		for(Neuron neuron : output.getNeurons()) {
			outputs[i] = neuron.getOutput();
			i++;
		}
		
		return outputs;
	}
	
	public ArrayList<Layer> getLayers() {
		return this.layers;
	}
}
