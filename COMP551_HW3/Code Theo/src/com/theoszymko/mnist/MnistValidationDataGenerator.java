package com.theoszymko.mnist;

import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;

import com.theoszymko.training.DataSet;
import com.theoszymko.training.TrainingDataGenerator;

public class MnistValidationDataGenerator extends TrainingDataGenerator {
	private int sampleSize;
	private double[][] inputs;
	private double[][] outputs;
	
	public MnistValidationDataGenerator(int sampleSize) {
		this.sampleSize = sampleSize;
		
		this.loadData();
	}
	
	public void loadData() {
		String csvFile = "mnist_test.csv";
        BufferedReader br = null;
        String line = "";
        String cvsSplitBy = ",";

        try {

            br = new BufferedReader(new FileReader(csvFile));
            int count = 0;
            this.inputs = new double[this.sampleSize][28 * 28];
            this.outputs = new double[this.sampleSize][10];
            
            while ((line = br.readLine()) != null && count < this.sampleSize) {

                // use comma as separator
                String[] data = line.split(cvsSplitBy);
                
                double[] input = new double[28 * 28];
                for(int k = 0; k < 28 * 28; k++) {
                	int v = Integer.valueOf(data[k+1]);
                	input[k] = v > 240 ? 255 : 0;
                }
                this.inputs[count] = input;
                
                double[] output = new double[10];
                int number = Integer.valueOf(data[0]);
                for(int k = 0; k < 10; k++) {
                	output[k] = (k == number ? 1 : 0);
                }
                this.outputs[count] = output;
                
                count++;

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
		return new DataSet(this.inputs, this.outputs);
	}
}
