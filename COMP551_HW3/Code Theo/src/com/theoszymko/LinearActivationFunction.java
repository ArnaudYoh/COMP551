package com.theoszymko;

public class LinearActivationFunction extends ActivationFunction {
	 public double activate(double weightedSum) {
	        return weightedSum;
	    }

	    public double derivative(double weightedSum) {
	        return 1;
	    }
}
