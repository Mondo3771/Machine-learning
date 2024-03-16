import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score

# Load the data
data_input = pd.read_csv('banknote_authentication.csv')

# Convert the data to a NumPy array
X = data_input.to_numpy()

# Print the shape of the data
data = np.array(X[0][0].split(';'))
for i in range(1, len(X)):
    data = np.vstack((data,np.array(X[i][0].split(';'))))
print(data)
np.random.shuffle(data)
x_values=np.array(data[:,:3])
y_values=np.array(data[:,-1])
print(x_values)
print(y_values)

gnb = GaussianNB()
l =int(len(x_values)*.8)
print(l)
gnb.fit(x_values[0 : l] , y_values[0 : l])

y_pred = gnb.predict(x_values[l : len(x_values)] )

# Output: (100, 5)