package com.theoszymko.mnist;

public class DigitImage {
	public double[] pixels = new double[28 * 28];
	
	public DigitImage(double[] pixels) {
		this.pixels = pixels;
	}
}
