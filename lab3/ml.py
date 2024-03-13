import numpy as np
import pandas as pd

# Load the data
data_input = pd.read_csv('banknote_authentication.csv')

# Convert the data to a NumPy array
X = data_input.to_numpy()

# Print the shape of the data
data = np.array(X[0][0].split(';'))
for i in range(1, len(X)):
    data = np.vstack((data,np.array(X[i][0].split(';'))))
print(data)

x_values=np.array(data[:,:3])
y_values=np.array(data[:,-1])
print(x_values)
print(y_values)
# Output: (100, 5)