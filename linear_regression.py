import csv
import sys
import matplotlib.pyplot as plt

min_x = 0
max_x = 0
min_y = 0
max_y = 0

theta0 = 0
theta1 = 0

learningRate = 0.01
nb_iterations = 10000

history_loss = []

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

def estimatedPrice(mileage):
    return theta0 + theta1 * mileage

def get_min_max(data):
    global min_x, max_x, min_y, max_y

    min_x = max_x = data[0][0]
    min_y = max_y = data[0][1]

    for mileage, price in data:

        if (mileage > max_x):
            max_x = mileage
        if (price > max_y):
            max_y = price
        if (mileage < min_x):
            min_x = mileage
        if (price < min_y):
            min_y = price

def normalizeData(data):
    data_normalized = []

    for mileage, price in data:
        mileage_normalized = (mileage - min_x) / (max_x - min_x)
        price_normalized = (price - min_y) / (max_y - min_y)
        data_normalized.append((mileage_normalized, price_normalized))    

    return data_normalized

def linear_regression(data):
    global theta0, theta1, learningRate
    m = len(data)

    prv_error_history = 1000
    limit = 1e-6

    for i in range(nb_iterations):
        tmp0 = 0
        tmp1 = 0
        error_history = 0

        for mileage, price in data:
            error = estimatedPrice(mileage) - price
            tmp0 += error
            tmp1 += error * mileage

            error_history += error * error

        if abs(prv_error_history - error_history) < limit:
            break
        prv_error_history = error_history
        history_loss.append((i, error_history))

        theta0 -= learningRate * (tmp0 / m)
        theta1 -= learningRate * (tmp1 / m)
        
def denormalizeTheta():
    global theta0, theta1
    theta1 = theta1 * ((max_y - min_y) / (max_x - min_x))
    theta0 = theta0 * (max_y - min_y) - theta1 * min_x + min_y
    print("theta0:", theta0, " theta1:", theta1)


def show_graph(data, history_loss):
    fig, axes = plt.subplots(1, 2, figsize=(10, 5))


    iterations, losses = zip(*history_loss)
    axes[1].plot(iterations, losses, 'b-', label="Loss Curve")
    axes[1].set_xlabel("Iterations")
    axes[1].set_ylabel("Loss Value")
    axes[1].set_title("Evolution of the loss value through the iterations")

    for line in data:
        km, price = line
        axes[0].plot(km, price, 'ro')
    
    nb_points = 100
    x_line = [i *(max_x - 0) / nb_points for i in range (nb_points + 1)]
    y_line = [theta1 * x + theta0 for x in x_line]
    axes[0].plot(x_line, y_line, color='red', label=f"y = {theta1}x + {theta0}")
    axes[0].set_xlabel("Mileage")
    axes[0].set_ylabel("Price")
    axes[0].set_title("Price based on mileage")


    plt.tight_layout()
    plt.show()

def store_theta():
    file_path = 'theta.csv'

    try:
        csvfile = open(file_path, mode='w', newline='', encoding='utf-8')
    except OSError:
        print ("Could not read file:", file_path)
        sys.exit()

    with csvfile:
        try:
            writer = csv.writer(csvfile)
            writer.writerow(['theta0', 'theta1'])
            writer.writerow([theta0, theta1])
        except csv.Error as e:
            print("Error wrinting in csv file:", e)
            sys.exit
    return data


if __name__ == "__main__":
    data = get_data()

    get_min_max(data)
    data_normalized = normalizeData(data)

    linear_regression(data_normalized)
    
    denormalizeTheta()
    store_theta()

    show_graph(data, history_loss)




