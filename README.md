# cs6111-project3

## I. About

Data mining refers to the process of trying to extract interesting/useful conclusions from a large 
database. Here, we attempt to "mine" association rules from a dataset containing [
New York City Restaurant Inspection Results](https://data.cityofnewyork.us/Health/DOHMH-New-York-City-Restaurant-Inspection-Results/43nn-pn8j)
found through the [NYC Open Data site](https://opendata.cityofnewyork.us/data/). 
All NYC restaurants are required to undergo inspection annual to be compliant with the food 
and safety obligations outlined in New York City Health Code Article 81. This dataset contains 
every sustained/not yet adjudicated violation citation for active restaurants for the last three 
years. This dataset is updated automatically on a daily basis by the Department of Health and 
Mental Hygiene (DOHMH).

## II. Design & Structure

### i. Data Set and Cleaning

Because the dataset selected represents "real world" data, we performed a series of cleaning steps
on the downloaded data before attempting to extract association rules. The following list
represents the steps, in order, that we took in cleaning the dataset, with an explanation:
1. Remove any rows that do not contain a valid borough. We know there are only five valid boroughs
in NYC (Staten Island, Manhattan, Queens, Brooklyn, Bronx), so every entry must contain one of this
enumerated list of locations.
2. Remove rows that are from inspections prior to 2018. The original dataset pulled from the NYC Open
Data website contained 395K rows, far more than we needed for this analysis (and also a larger `.csv`
file than is allowed by github.com); hence, we narrowed the dataset to this date range. This cleaning
step includes the removal of rows with inspection dates of 1/1/1900, which represent the "dummy" value
for new restaurants that have not yet received an inspection, but which are still included in the 
dataset.
3. Because the dataset includes a number of columns with numeric values, we decided to "bucket" the
values into several numeric ranges. For example:
    * 
4. In order to make the extracted results more readable and clear, we decided to append the column
name to data entry. For example, an entry in the Critical Flag column with `N` became `Critical Flag: N`
in the analyzed dataset to facilitate analysis of the final association rules.
5. Remove columns that contain duplicate information/identifiers. Note that the original dataset was
 not fully normalized; for example, the dataset included a unique DOHMH identifier for the restaurant as 
 well as the restaurant's name. If we ran the association rules script on this data, we would likely
 get the uninteresting result that a restaurant's DOHMH identifier implies the restaurant name. The same
 is true for the violation code/description. Hence, we decided to remove 

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
