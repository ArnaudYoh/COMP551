package com.theoszymko;

public class ThresoldActivationFunction extends ActivationFunction {
	private double thresold;
	
	public ThresoldActivationFunction(double thresold) {
		this.thresold = thresold;
	}

	@Override
	public double activate(double x) {
		return x > thresold ? 1 : 0;
	}

	@Override
	public double derivative(double x) {
		return 0;
	}

}
