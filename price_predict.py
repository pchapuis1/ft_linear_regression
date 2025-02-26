import csv

def get_theta():
    file_path = 'theta.csv'
    theta = []

    try:
        with open(file_path, mode='r') as csvfile:
            datareader = csv.reader(csvfile, delimiter=',')
            next(datareader) 
            for line in datareader:
                try:
                    values = tuple(float(value) for value in line)
                    theta.append(values)
                except ValueError:
                    print("Conversion error for line:", line)
    except (OSError, csv.Error) as e:
        print("Error reading csv file:", e)
        return None

    return theta if theta else None

theta = get_theta()
if theta is None:
    print("Could not load theta values.")
    exit(1)

while True:
    mileage_asked = input("Enter mileage: ")
    try:
        mileage_float = float(mileage_asked)
        if mileage_float > 0:
            break
        else:
            print("The mileage can't be negative.")
    except ValueError:
        print("Enter a valid number.")

price_predicted = theta[0][0] + mileage_float * theta[0][1]
print("The price predicted is:", price_predicted)
