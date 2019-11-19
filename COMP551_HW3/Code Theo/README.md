## How to get the data

You must have two files:

- `train_x.bin` (from kaggle)
- and also the `.csv` format for the mnist data from http://pjreddie.com/projects/mnist-in-csv/ and rename them `mnist_train.csv` and `mnist_test.csv`

Launching the java program will loop for weights to load.

Here are the options for the java program:

-  `-layers <1> <2> ..` define the size of the layers
- `-train` training mode
- `-traingSize` training size to load (no typo)
- `-dropout <double>` dropout parameter
- `-maxEpoch <int>` number maximum nubmer of epochs
- `-kaggleSize <int>` size of the kaggle test 