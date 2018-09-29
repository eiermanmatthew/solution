import csv, os
import datetime
import dateparser
import re

## validate date format is valid if it is valid return isoformat date else empty
def validate(date_text):
    if len(re.findall(r"[\w']+", date_text)) > 2:
        dt = dateparser.parse(date_text, date_formats=['%B %-d, %Y', '%m/%d/%Y', '%Y-%m-%d'])
        if dt is not None:
            return dt.strftime('%Y-%m-%d')
    return ""

## Read csv file and return states dictionary with abbreviations as key
def get_states(filename):
    states = {}
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count > 0:
                states[row[0]] = row[1]
            line_count += 1
    return states

## Create csv file
def write_csv(filename, header, data):
        """Write CSV file to working dir."""
        with open(filename, 'wb') as fh:
            writer = csv.writer(fh)
            writer.writerow(header)
            for row in data:
                writer.writerow(row)

## read and clean up data
def read_csv(filename):
    data = []
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            print "Processing row: "+str(line_count)
            processed_row = []
            if line_count > 0:
                row[5] = states.get(row[5])
                row[8] = ' '.join(row[8].split())
                valid_date = validate(row[10])
                if valid_date == "":
                    row.append(row[10])
                    row[10] = ""
                else:
                    row.append("")
                    row[10] = valid_date
                data.append(row)
            line_count += 1
    return data

## get file paths from users
def get_user_input(type):
    filename = str(raw_input("Enter "+type+" csv file path: "))
    while not os.path.exists(filename):
        print "Invalid Path: "+filename
        filename = str(raw_input("Enter "+type+" csv file path: "))
    return filename


states = get_states(get_user_input("state abbreviations"))
data = read_csv(get_user_input("data"))
write_csv('enriched.csv', ['name', 'gender', 'birthdate', 'address', 'city', 'state', 'zipcode', 'email', 'bio', 'job', 'start_date', 'start_date_description'], data)
print "enriched.csv is created successfully"
