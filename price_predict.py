import csv

def get_theta():
    file_path = 'theta.csv'
    theta = []

    try:
        with open(file_path, mode='r') as csvfile:
            datareader = csv.reader(csvfile, delimiter=',')
            next(datareader) 
            for line in datareader:
                if len(line) != 2:
                    print("Invalid line in theta file:", line)
                    return None
                try:
                    values = tuple(float(value) for value in line)
                    theta.append(values)
                except ValueError:
                    print("Conversion error for line:", line)
    except (OSError, csv.Error) as e:
        return None
    return theta if theta else None

theta = get_theta()
if theta is None:
    theta = [(0.0, 0.0)]

while True:
    km_asked = input("Enter mileage: ")
    try:
        km_value = float(km_asked)
        if km_value > 0:
            break
        else:
            print("The mileage can't be negative.")
    except ValueError:
        print("Enter a valid number.")

price_predicted = theta[0][0] + km_value * theta[0][1]
print("The price predicted is:", price_predicted)
