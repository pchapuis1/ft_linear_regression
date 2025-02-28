import csv
import sys
import matplotlib.pyplot as plt

class LinearRegression:
    def __init__(self):
        self.theta0 = 0
        self.theta1 = 0
        self.learning_rate = 0.01
        self.nb_iterations = 10000
        self.min_x = 0
        self.max_x = 0
        self.min_y = 0
        self.max_y = 0
        self.history_loss = []
        self.data = []
        self.data_normalized = []

    def get_data(self):
        file_path = 'data.csv'

        try:
            with open(file_path, 'r') as csvfile:
                try:
                    datareader = csv.reader(csvfile, delimiter = ',')
                    next(datareader)
                    for line in datareader:
                        if not any(line) or len(line) != 2:
                            continue
                        try:
                            values = tuple([int(value) for value in line])
                            self.data.append(values)
                        except ValueError:
                            print("Conversion error for line:", line)
                except csv.Error as e:
                    print("Error reading csv file:", e)
                    sys.exit()
        except OSError:
            print ("Could not read file:", file_path)
            sys.exit()


    def estimatedPrice(self, mileage):
        return self.theta0 + self.theta1 * mileage

    def get_min_max(self):
        if (len(self.data) < 2):
            print("Error: Need at least 2 observations to train the model!")
            sys.exit()

        self.min_x = self.max_x = self.data[0][0]
        self.min_y = self.max_y = self.data[0][1]

        for mileage, price in self.data:
            if (mileage > self.max_x):
                self.max_x = mileage
            if (price > self.max_y):
                self.max_y = price
            if (mileage < self.min_x):
                self.min_x = mileage
            if (price < self.min_y):
                self.min_y = price

    def normalizeData(self):
        for mileage, price in self.data:
            mileage_normalized = (mileage - self.min_x) / (self.max_x - self.min_x)
            price_normalized = (price - self.min_y) / (self.max_y - self.min_y)
            self.data_normalized.append((mileage_normalized, price_normalized))    

    def linear_regression(self):
        m = len(self.data_normalized)
        prv_error_history = 1000
        limit = 1e-6

        for i in range(self.nb_iterations):
            tmp0 = 0
            tmp1 = 0
            error_history = 0

            for mileage, price in self.data_normalized:
                error = self.estimatedPrice(mileage) - price
                tmp0 += error
                tmp1 += error * mileage

                error_history += error * error

            if abs(prv_error_history - error_history) < limit:
                break
            prv_error_history = error_history
            self.history_loss.append((i, error_history))

            self.theta0 -= self.learning_rate * (tmp0 / m)
            self.theta1 -= self.learning_rate * (tmp1 / m)
        
    def denormalizeTheta(self):
        self.theta1 = self.theta1 * ((self.max_y - self.min_y) / (self.max_x - self.min_x))
        self.theta0 = self.theta0 * (self.max_y - self.min_y) - self.theta1 * self.min_x + self.min_y

    def show_graph(self):
        fig, axes = plt.subplots(1, 2, figsize=(10, 5))

        iterations, losses = zip(*self.history_loss)
        axes[1].plot(iterations, losses, 'b')
        axes[1].set_xlabel("Iterations")
        axes[1].set_ylabel("Loss Value")
        axes[1].set_title("Evolution of the loss value through the iterations")

        for line in self.data:
            km, price = line
            axes[0].plot(km, price, 'ro')
        
        nb_points = 100
        x_line = [i *(self.max_x - 0) / nb_points for i in range (nb_points + 1)]
        y_line = [self.theta1 * x + self.theta0 for x in x_line]
        axes[0].plot(x_line, y_line, 'r')
        axes[0].set_xlabel("Mileage")
        axes[0].set_ylabel("Price")
        axes[0].set_title("Price based on mileage")

        plt.tight_layout()
        plt.show()

    def store_theta(self):
        file_path = 'theta.csv'

        try:
            with open(file_path, mode='w', newline='') as csvfile:
                try:
                    writer = csv.writer(csvfile)
                    writer.writerow(['theta0', 'theta1'])
                    writer.writerow([self.theta0, self.theta1])
                except csv.Error as e:
                    print("Error wrinting in csv file:", e)
                    sys.exit()
        except OSError:
            print ("Could not read file:", file_path)
            sys.exit()

def main():
    linearRegression = LinearRegression()

    linearRegression.get_data()
    linearRegression.get_min_max()
    linearRegression.normalizeData()

    # Train the model
    linearRegression.linear_regression()
    
    linearRegression.denormalizeTheta()
    linearRegression.store_theta()
    linearRegression.show_graph()

if  __name__ == "__main__":
    main()