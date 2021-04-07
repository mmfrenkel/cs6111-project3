# cs6111-project3: Mining Association Rules

## I. About

Data mining refers to the process of trying to extract interesting/useful conclusions from a large 
database. Here, we attempt to "mine" association rules from a dataset containing [
New York City Restaurant Inspection Results](https://data.cityofnewyork.us/Health/DOHMH-New-York-City-Restaurant-Inspection-Results/43nn-pn8j)
found through the [NYC Open Data site](https://opendata.cityofnewyork.us/data/). 
All NYC restaurants are required to undergo inspection annual to be compliant with the food 
and safety obligations outlined in New York City Health Code Article 81. This dataset contains 
every sustained/not yet adjudicated violation citation for active restaurants for the last three 
years (2018-2021). This dataset is updated automatically on a daily basis by the Department of Health and 
Mental Hygiene (DOHMH).

The final, cleaned dataset that we used to generate association rules as part of this project can be found
in `./project/data/restaurant_data_lim.csv`. Note that while we decided to use this specifc dataset, this program is
written generically enough to handle any cleaned dataset in .csv format with comma-separated values.

## II. Design & Structure

### i. Data Set and Cleaning

Because the dataset selected represents "real world" data, we performed a series of cleaning steps
on the data downloaded directly from the NYC Open Data Site before attempting to extract association rules. 
The following list represents the steps, in order, that we took in cleaning the dataset:
1. Remove any rows that do not contain a valid borough: We know there are only five valid boroughs
in NYC (Staten Island, Manhattan, Queens, Brooklyn, Bronx), so every entry must contain one of this
enumerated list of locations.
2. Remove rows that are from inspections prior to 2018: The original dataset pulled from the NYC Open
Data website contained 395K rows, far more than we needed for this analysis; hence, we narrowed the 
dataset to this date range. This cleaning step included the removal of rows with inspection dates of 
1/1/1900, which represent the "dummy" value for new restaurants that have not yet received an inspection, 
but which are still included in the  dataset.
3. Bucket values: Because the dataset includes a number of columns with numeric values, we decided to "bucket" the
values into several numeric ranges. However, later analysis showed that this data was neither 
interesting nor helpful, so we ended up removing our bucketed columns in the final, cleaned dataset.
4. Append Column Names: In order to make the extracted results more readable and clear, we decided to 
append the column name to data entry. For example, we append "Inspection Date: " to entries in the `INSPECTION_DATE` 
column to facilitate analysis of the final association rules (i.e., so that we understand that 2018 is a 
date, not any other numeric value). We did the same "data labeling" exercise for other columns that were 
not entirely clear, including merging violation code with violation description to create the final
`VIOLATION_DESCRIPTION` column in the dataset.
5. Remove columns that contain duplicate information/identifiers: The original dataset was
 not fully normalized; for example, the dataset included a unique DOHMH identifier for the restaurant as 
 well as the restaurant's name. If we ran the association rules program on this data, we would almost
 certainly get the uninteresting result that a restaurant's DOHMH identifier implies the restaurant name. 
 The same is true for the violation code/description and zipcode/borough. Hence, we decided to remove
 columns that did not provide any new information. 
6. Remove unhelpful columns: We removed any columns that contained information that was either (a) incomplete or 
(b) did not contain a diverse set of information. For example, the `GRADE` column of the original dataset
was incomplete; since we were more interested in the relationship between borough/restaurant/cuisine and 
violations, and not in the final grade, we were comfortable removing this column. As another example,
consider the `ACTION` and `INSPECTION TYPE` columns: there were only a few, limited options for these
values and most of the rows had the same value. This meant that association rules were inevitably going
to be generated, despite the fact that they would not likely be interesting results. As a result you
can see several iterations of the dataset in `/project3/data/` that reflect our iterations of cleaning
and simplifying the data over time.

Note: A subset of explicit cleaning steps outlined above is available here: `/project3/data/data_clean_up_restaurants.sql`. 

### ii. Internal Design 

Users interact with our program through the "cli layer", which acts as a user-friendly wrapper for 
the underlying `DataMiner` class. The cli layer is able to perform some rudimentary validation on the 
parameters to the program and provide some helpful suggestions for how to use the tool. The cli 
layer is also responsible for handling I/O (reading in files and printing out results to the user).
See section **V. Run** to see more information on how users interact with the cli layer.

Once a path to a valid `.csv` is obtained, the cli layer read in the specified .csv file as a pandas 
dataframe and passes it, along with the minimum support and confidence specifications, to an instance of 
the `DataMiner` class. The `DataMiner` instance is then called upon to generate the large itemsets 
for the data just the minimum support (`min_supp`) provided as a support threshold.

In order to generate large itemsets, the `DataMiner` uses the a-priori algorithm outlined in Section 2.1.1
Agrawal and Srikant (1994). The algorithm proceeds as follows:
1. Determine large 1-itemsets (k = 1, i.e., the first pass through the data) by looking at each 
individual item, counting the number of occurrences, and keeping only items with 
support >= min_supp.
2. For each future iteration (k > 1), the pass occurs in two phases:
    1. Determine the candidate k-itemsets via the `DataMiner` class' `_apriori_gen` function. This function
    itself has two primary steps. In the `join` step, the large (k-1)-itemsets are joined with itself
    in a SQL-like fashion to generate candidates. Then, in the `prune` step, any candidates that have 
    a subset that is not large are removed. This utilizes the key, basic intuition behind the a-priori
    algorithm that any subset of a large itemset must also be large.
    2. Determine which of the candidate k-itemsets are "large" by scanning the database to determine
    the support for each candidate. Note that we did not implement the subset function from Section
    2.1.1 of Agrawal and Srikant (1994) and instead use a simpler approach of comparing elements within 
     each transaction with the candidate itemset contents. Only candidate k-itemsets that reach the
     support threshold are kept around to serve as the "seed" for the next itemset iteration.
3. Through each iteration, a dictionary mapping larget itemsets to count in the database is updated. This allows
 the support for each large itemset to be stored for the next step of data processing, the generation
 of assocation rules.
4. Once there are no more large itemsets to consider, the loop stops and all large itemsets are returned.
   
Once the large itemsets are generated and returned back to the cli layer to be printed to the user,
the cli layer once again calls upon the `DataMiner` class to find the "high confidence" rules. The `DataMiner` 
builds all possible association rules that have exactly one item on the right side and at least
one item on the left side, where the right-side item does not appear on the left side.
Only association rules with confidence above `min_conf` are considered "high-confidence" and
returned to the cli layer.

The cli layer, upon receiving the final results from the `DataMiner`, prints out the results to the user.

## III. Files

### i. Setup Files
* `requirements.txt`: Requirements file, containing relevant dependencies for the project (see below)

### ii. Data Files

* `/project3/data/restaurant_inspection_data.csv`: The cleaned, final data set used for association
rule generation

### iii. Functionality
* `cli.py`: The main cli entrypoint for running the program as a user
* `data_miner.py`: Contains the central `DataMiner` class that performs the "heavy lifting" associated
with the data mining operation
* `itemsets.py`: Contains helper `KItemsets` class that is used to represent candidate and actual 
itemsets at each iteration
* `rules.py`: Contains a custom `Rules` class designed to hold the final association rule result

### iv. Dependencies
* `plumbum`: Library for supporting easy parsing of command line arguments
* `black`: Style checking and bug finding tool (note that this can be installed via `pip3 install black`,
but it is otherwise excluded from the `requirements.txt` file because it is not strictly necessary)
* `pandas`: Enables easy conversion of .csv file containing data into a data frame format, which in 
turn allows easy processing of the data 

## IV. Setup

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

## V. Run

To run the program, users should invoke the program by specifying a series of switches and 
arguments, as outlined below. The usage, generalized, is:
```
$ (venv) python -m project3.cli [SWITCHES]
```
Where `[SWITCHES]` correspond to the following **optional** command line arguments and values:

* `-d`, `--dataset`: (optional) A path to a .csv to process. By default, the program uses the main
 dataset mined in this project, found in `/project3/data/restaurant_inspection_data_lim.csv`.
* `-s`, `--minimum_support`: (optional) Specify a minimum support value (float, 0-1)".
* `-c`, `--minimum_confidence`: (optional) Specify a minimum confidence value (float, 0-1)".

By default, the program will run with the data and parameters we have preset (i.e., the default data 
is our cleaned restaurant dataset and a support of `0.1` and confidence of `0.2` are used).

**Note**: Depending on the size of the dataset, the association rule generation can take some time.
The default dataset completes in 5-10 minutes.

## VI. Results

When we found this dataset, we were intrigued by the opportunity to learn what, if any, associations
exist between boroughs/cuisines and different restaurant health code violations in New York City.
See sample results in `./project3/results/output.txt` from running the program with a minimum
support of 0.1 and minimum confidence of 0.2.

Here are several excerpts from our `output.txt` file that we found interesting:

##### 1. American Restaurant Violations 
Although we did not see a wide set of cuisines represented in our association rule results, we found
one cuisine commonly associated with restaurant violations: American food.
For example, consider the results below, which suggest that there is a relationship between 
American restaurants in Manhattan and violation 10F. Less specific to Manhattan restaurants, 
it also appears that there is a relationship between American restaurants and and violations 06D,
08A, 04N. These violations represent contamination, vermin, and flies respectively. It is
interesting that American food is the only cuisine specifically associated with violations.
```
Association Rule #7
* Rule: ['American', 'Violation 10F: Non-food contact surface improperly
constructed. Unacceptable material used. Non-food contact surface or equipment
improperly maintained and/or not properly sealed, raised, spaced or movable to
allow accessibility for cleaning on all sides, above and underneath the unit.']
=> ['Manhattan']
* Metrics: (Conf: 52.3%, Sup: 1.5%)
...
Association Rule #34
* Rule: ['Manhattan', 'Violation 10F: Non-food contact surface improperly
constructed. Unacceptable material used. Non-food contact surface or equipment
improperly maintained and/or not properly sealed, raised, spaced or movable to
allow accessibility for cleaning on all sides, above and underneath the unit.']
=> ['American']
* Metrics: (Conf: 25.3%, Sup: 1.5%)
...
Association Rule #37
* Rule: ['Violation 06D: Food contact surface not properly washed, rinsed and
sanitized after each use and following any activity when contamination may have
occurred.'] => ['American']
* Metrics: (Conf: 24.8%, Sup: 1.8%)
...
Association Rule #41
* Rule: ['Manhattan', 'Violation 08A: Facility not vermin proof. Harborage or
conditions conducive to attracting vermin to the premises and/or allowing vermin
to exist.'] => ['American']
* Metrics: (Conf: 24.5%, Sup: 1.1%)
...
Association Rule #53
* Rule: ['Violation 04N: Filth flies or food/refuse/sewage-associated (FRSA)
flies present in facility’s food and/or non-food areas. Filth flies include
house flies, little house flies, blow flies, bottle flies and flesh flies.
Food/refuse/sewage-associated flies include fruit flies, drain flies and Phorid
flies.'] => ['American']
* Metrics: (Conf: 21.8%, Sup: 1.1%)
```

##### 2. Mice Everywhere
Another interesting observation is that it appears that restaurants throughout the borough's 
are plagued by mice. As shown below, there is evidence of violation 04L in Manhattan, Brooklyn
and Queens, suggesting that this is a problem that shows up all over the city -- for those who
live in NYC, this comes as no surprise, though it is interesting that the data supports it.
```
Association Rule #18
* Rule: ["Violation 04L: Evidence of mice or live mice present in facility's
food and/or non-food areas."] => ['Manhattan']
* Metrics: (Conf: 36.7%, Sup: 2.9%)
...
Association Rule #28
* Rule: ["Violation 04L: Evidence of mice or live mice present in facility's
food and/or non-food areas."] => ['Brooklyn']
* Metrics: (Conf: 26.9%, Sup: 2.1%)
...
Association Rule #43
* Rule: ["Violation 04L: Evidence of mice or live mice present in facility's
food and/or non-food areas."] => ['Queens']
* Metrics: (Conf: 23.7%, Sup: 1.9%)
```
##### Other Comments

Alongside these interesting results, our program also generates a series of high confidence 
association rules that are not interesting and insightful; for example `DUNKIN => Donuts` (most
people know that DUNKINs serves donuts already.

This demonstrates how although programs can be written to generate association rules, human 
judgements and knowledge of the relevant domain of the dataset are required to pick out the 
interesting association rule.

## VII. Credits

This project was completed as part of an assignment for Advanced Databases (CS6111), a course taught 
at Columbia University by Professor Luis Gravano in Spring 2021. The concept for this project and 
several of the parameters were derived from the assignment available [here](http://www.cs.columbia.edu/~gravano/cs6111/proj3.html).

Source:
Argawal, R., Srikant, R., Fast Algorithms for Mining Association Rules, VLDB (1994).
