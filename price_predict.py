
theta0 = 1
theta1 = 4


valid_input = False

while valid_input == False:
    mileage_asked = input("Enter mileage: ")
    try:
        mileage_float = float(mileage_asked)
        if (mileage_float > 0) :
            valid_input = True
        else :
            print ("The mileage can't be negative.")
    except ValueError:
        print("Enter a valid number.")

print ("The price predicted is:", theta0 + mileage_float * theta1)