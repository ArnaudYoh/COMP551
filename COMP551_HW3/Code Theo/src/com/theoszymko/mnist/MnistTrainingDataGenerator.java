package com.theoszymko.mnist;

import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Random;

import com.theoszymko.training.DataSet;
import com.theoszymko.training.TrainingDataGenerator;

public class MnistTrainingDataGenerator extends TrainingDataGenerator {
	private int sampleSize;
	private double[][] inputs;
	private double[][] outputs;
	int[] digits = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9};
	
	HashMap<Integer, ArrayList<DigitImage>> labelToDigits;
	
	public MnistTrainingDataGenerator(int sampleSize) {
		this.sampleSize = sampleSize;
		this.labelToDigits = new HashMap<Integer, ArrayList<DigitImage>>(); 
		
		this.loadData();
	}
	
	public void loadData() {
		String csvFile = "mnist_train.csv";
        BufferedReader br = null;
        String line = "";
        String cvsSplitBy = ",";

        try {

            br = new BufferedReader(new FileReader(csvFile));
            int count = 0;
            
            while ((line = br.readLine()) != null && count < this.sampleSize) {

                // use comma as separator
                String[] data = line.split(cvsSplitBy);
                
                // removing noise
                double[] input = new double[28 * 28];
                for(int k = 0; k < 28 * 28; k++) {
                	int v = Integer.valueOf(data[k+1]);
                	input[k] = v > 240 ? 255 : 0;
                }
                
                int number = Integer.valueOf(data[0]);
                
                if(this.labelToDigits.get(number) == null) {
                	this.labelToDigits.put(number, new ArrayList<DigitImage>());
                }
                
                this.labelToDigits.get(number).add(new DigitImage(input));
                count++;
            }
            
            for(int k = 0; k < 10; k++) {
            	System.out.println("Loaded "+this.labelToDigits.get(k).size()+" images for label "+k);
            }

        } catch (FileNotFoundException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            if (br != null) {
                try {
                    br.close();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }
	}

	@Override
	public DataSet getDataSet() {
		int sampleSize = 10;
		this.inputs = new double[sampleSize][28 * 28];
		this.outputs = new double[sampleSize][10];
		
		this.digits = shuffle(this.digits);
		int lengthOfDigits = 9;
		
		for(int i = 0; i < sampleSize; i++) {
			int index = i % lengthOfDigits;
			outputs[i] = this.getOneHotFor(this.digits[index]);
			inputs[i] = randomImageForLabel(this.digits[index]).pixels;
		}
		
		return new DataSet(this.inputs, this.outputs);
	}
	
	public DigitImage randomImageForLabel(int label) {
		Random random = new Random();
        ArrayList<DigitImage> images = this.labelToDigits.get(label);
        return images.get(random.nextInt(images.size()));
	}
	
	private int[] shuffle(int[] array) {

        Random random = new Random();
        for(int i = array.length - 1; i > 0; i--) {

            int index = random.nextInt(i + 1);

            int temp = array[i];
            array[i] = array[index];
            array[index] = temp;
        }

        return array;
    }
	
	public double[] getOneHotFor(int label) {
		double[] oneHot = new double[] {0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
		oneHot[label] = 1;
		return oneHot;
	}
}
