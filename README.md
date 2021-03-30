# cs6111-project3

## I. About

## II. Internal Design & Structure

## III. Files

### i. Setup Files
* `requirements.txt`: Requirements file, containing relevant dependencies for the project (see below)

### ii. Functionality
* `cli.py`: The main cli entrypoint for running the program as a user
* `data_miner.py`: Contains the central `DataMiner` class that performs the "heavy lifting" associated
with the data mining operation
* `itemsets.py`: Contains helper `KItemsets` class that is used to represent candidate and actual 
itemsets at each iteration, k

### iii. Dependencies
* `plumbum`: Library for supporting easy parsing of command line arguments
* `black`: Style checking and bug finding tool
* `pandas`: Enables easy conversion of .csv file containing data into a data frame format, which in 
turn allows easy processing of the data 

## Setup

Please note that this project is intended to run on a Ubuntu 18.04 LTS Google Cloud VM.

### i. Environment 

This project requires python4. Make sure that python3 and associated packages are installed 
correctly on your linux machine (you do not need to do this if your machine is already setup):
```
$ sudo apt-install pip3-pip
$ sudo apt-install python3-virtualenv
```

Now make sure that your environment is setup correctly by first creating a new virtual environment 
and then pip-installing the dependencies outlined in the provided `requirements.txt`
file:
```
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

## Run

To run the program, users should invoke the program by specifying a series of switches and 
arguments, as outlined below. The usage, generalized, is:
```
$ (venv) python -m project3.cli [SWITCHES]
```
Where `[SWITCHES]` correspond to the following mandatory command line arguments and values:

* `-d`, `--dataset`: (optional) A path to a .csv to process. By default, the program uses the main
 dataset mined in this project, found in `/project3/data/restaurant_inspection_data.csv`.
* `-s`, `--minimum_support`: (optional) Specify a minimum support value (float, 0-1)".
* `-c`, `--minimum_confidence`: (optional) Specify a minimum confidence value (float, 0-1)".
