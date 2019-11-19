package com.theoszymko.mnist;

import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.Arrays;

import com.theoszymko.training.DataSet;
import com.theoszymko.training.TrainingDataGenerator;

public class KaggleTrainingDataGenerator extends TrainingDataGenerator {
	private int sampleSize;
	private double[][] inputs;
	private double[][] outputs;
	
	public KaggleTrainingDataGenerator(int sampleSize) {
		this.sampleSize = sampleSize;
		
		this.loadData();
	}
	
	public void loadData() {
		String csvFile = "train_x.csv";
        BufferedReader br = null;
        String line = "";
        String cvsSplitBy = ",";

        try {

            br = new BufferedReader(new FileReader(csvFile));
            int count = 0;
            this.inputs = new double[this.sampleSize][60 * 60];
            
            while ((line = br.readLine()) != null && count < this.sampleSize) {

                // use comma as separator
                String[] data = line.split(cvsSplitBy);
                
                double[] input = new double[60 * 60];
                for(int k = 0; k < 60 * 60; k++) {
                	int v = Integer.valueOf(data[k]);
                	input[k] = v < 240 ? 0 : 255;
                }
                this.inputs[count] = input;
                
                System.out.println(Arrays.toString(input));
                
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
        
        csvFile = "train_y.csv";
        br = null;
        line = "";
        cvsSplitBy = ",";

        try {

            br = new BufferedReader(new FileReader(csvFile));
            int count = 0;
            this.outputs = new double[this.sampleSize][1];
            br.readLine(); // flush first line
            
            while ((line = br.readLine()) != null && count < this.sampleSize) {

                // use comma as separator
                String[] data = line.split(cvsSplitBy);
                
                this.outputs[count][0] = Integer.valueOf(data[1]);
                
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
