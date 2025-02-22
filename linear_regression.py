import csv
import sys
import matplotlib.pyplot as plt

theta0 = 0
theta1 = 0

learningRate = 0.00000001

max_x = 0
max_y = 0


def get_data():

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
                    values = tuple([int(value) for value in line])
                    data.append(values)
                except ValueError:
                    print("Conversion error for line:", line)
        except csv.Error as e:
            print("Error reading csv file:", e)
            sys.exit
    return data

def estimatedPrice(x):
    return (theta0 + theta1 * x)

epochs = 1000

def linear_regression(data):
    global theta0, theta1, learningRate
    m = len(data)

    for _ in range(epochs):
        tmp0 = 0
        tmp1 = 0
        for line in data:
            mileage, price = line
            error = estimatedPrice(mileage) - price
            tmp0 += error
            tmp1 += error * mileage

        theta0 -= learningRate * (tmp0 / m)
        theta1 -= learningRate * (tmp1 / m)
        print("theta0:", theta0, " theta1:", theta1)


    print("theta0:", theta0, " theta1:", theta1)
        


def get_min_max(data):
    global max_x, max_y

    for line in data:
        km, price = line
        if (km > max_x):
            max_x = km
        if (price > max_y):
            max_y = price

def show_graph(data):
    
    for line in data:
        km, price = line
        plt.plot(km, price, 'ro')

    nb_points = 100
    x_line = [i *(max_x - 0) / nb_points for i in range (nb_points + 1)]
    y_line = [theta1 * x + theta0 for x in x_line]
    plt.plot(x_line, y_line, color='red', label=f"y = {theta1}x + {theta0}")


    plt.xlabel("Mileage")
    plt.ylabel("Price")
    plt.title("Prix en fonction du kilometrage")
    plt.show()
    plt.close()

if __name__ == "__main__":
    data = get_data()

    linear_regression(data)
    get_min_max(data)
    show_graph(data)

