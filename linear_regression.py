import csv
import sys

file_path = 'data.csv'

data = []

try:
    csvfile = open(file_path, 'r')
except OSError:
    print ("Could not read file:", file_path)
    sys.exit()

with csvfile:
    try:
        datareader = csv.reader(csvfile, delimiter = ',')
        next(datareader)
        for line in datareader:
            try:
                values = tuple([float(value) for value in line])
                data.append(values)
            except ValueError:
                print("Conversion error for line:", line)
    except csv.Error as e:
        print("Error reading csv file:", e)
        sys.exit

for line in data:
    km, price = line
    total = km + price
    print(f"Ligne : {line}, Somme : {total}")
