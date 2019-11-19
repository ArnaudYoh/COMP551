package com.theoszymko;

public class SigmoidActivationFunction extends ActivationFunction {
	@Override
	public double activate(double t) {
		return 1.0d / (1.0d + Math.exp(-t));
	}

	@Override
	public double derivative(double t) {
		return t * (1.0d - t);
	}
}
