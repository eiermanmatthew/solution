# CSV Processing

This is a **Python 2** CSV Cleaning application. We strongly recommend creating a virtualenv before performing the steps below.

## Install requirements

`pip install -r requirements.txt`


## Run the scrapper

`python clean_csv.py`

User Input: Script ask user to input state abbreviations and data csv files

"Enter state abbreviations csv file path: "

"Enter state data file path: "

Once data is file paths are provided script will clean up data according to requirements and generate enriched csv. 
Rules for clean up are:

a. String Cleaning
b. Code swap
c. Date offset


