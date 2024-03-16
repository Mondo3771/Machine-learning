import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt
from scipy.stats import norm 
import statistics as st

# Load the data
data_input = pd.read_csv('banknote_authentication.csv')

# Convert the data to a NumPy array
X = data_input.to_numpy()

data = np.array(X[0][0].split(';'))
for i in range(1, len(X)):
    data = np.vstack((data,np.array(X[i][0].split(';'))))
np.random.shuffle(data)
data = data.astype(float)
# this sepreates the data into forged and real thingies

data_1  = data[data[:,-1]==1]
data_0  = data[data[:,-1] == 0]

# var_1 = data_1[:,0]
# var_0 = data_0[:,0]
# skew_1 = data_1[:,1]
# skew_0 = data_0[:,1]
# cont_1 = data_1[:,2]
# cont_0 = data_0[:,2]
# entropy_1 = data_1[:,3]
# entropy_0 = data_0[:,3]

# y = skew_0
# plt.plot(var_0, skew_0, '.', color='black')
# plt.plot(var_1, skew_1, '.', color='red')

# # plt.show()


#  sperates into x and y values
x_values=np.array(data[:,:4])
y_values=np.array(data[:,-1])
l = int(len(x_values)*.8)


x_train_1 = data_1[:,:4][:l]
y_train_1 =data_1[:,-1][:l]
x_train_0 = data_0[:,:4][:l]
y_train_0 =data_0[:,-1][:l]

x_test = np.array(x_values[l : len(x_values)])
y_test = np.array(y_values[l : len(y_values)])

# Calculate the priors of the data 
prior_1 = len(data_1)/len(data)
prior_0 = len(data_0)/len(data)
# we are making the model for the 1 assume ecevything is gaussian 
# we create the mean an variance of the model using the training data where class ==1
means_1 = np.array([0.0,0.0,0.0,0.0])# the reason we have 4 elements is becasue each index corresponds to eiter varinace skewness etc
vars_1 = np.array([0.0,0.0,0.0,0.0])
for i in range(4):
    x = np.array(x_train_1[:,i])
    mean = st.mean(x)
    means_1[i] = mean
    var = st.variance(x)
    vars_1[i] = var
# we are making the model for the 0 assume ecevything is gaussian 
# we create the mean an variance of the model using the training data where class ==0
means_0 = np.array([0.0,0.0,0.0,0.0]) #
vars_0 = np.array([0.0,0.0,0.0,0.0])

for i in range(4):
    x = np.array(x_train_0[:,i])
    mean = st.mean(x)
    means_0[i] = mean
    var = st.variance(x)
    vars_0[i] = var
prob_1 = 1
prob_0 = 1
cr=0
confusion_matrix=np.zeros((2,2))
print(confusion_matrix)
for i in  range(0,len(x_test)):
    for j in range(4):
        var = x_test[i][j]
        m_1 = means_1[j]
        v_1 = vars_1[j]
        m_0 = means_0[j]
        v_0 = vars_0[j]

        prob_var_given_1 = 1/math.sqrt(2*math.pi*v_1)
        prob_var_given_1  *= math.e**(-0.5*((var-m_1)**2)/v_1)
        p_0 = 1/math.sqrt(2*math.pi*v_0)
        p_0 *= math.e**(-0.5*((var-m_0)**2)/v_0)

        prob_1 *= prob_var_given_1
        prob_0 *= p_0

    prob = (prob_1*prior_1)/(prob_1*prior_1 + prob_0*prior_0 ) 
    # print("probabilty that it is 1: ",prob)
    if (prob > 1-prob):
        print("Predicted : 1")
        if(y_test[i] == 1):
            cr+=1
            confusion_matrix[1][1]+=1
            for k in range(4):
                x_train_1 = np.vstack((x_train_1, x_test[i]))
                x = np.array(x_train_1[:,k])
                mean = st.mean(x)
                means_1[k] = mean
                var = st.variance(x)
                vars_1[k] = var
        else:
            confusion_matrix[1][0]+=1
    else:
        print("Predicted : 0")
        if(y_test[i] == 0):
            cr+=1
            confusion_matrix[0][0]+=1
            for k in range(4):
                x_train = np.vstack((x_train_0, x_test[i]))
                x = np.array(x_train_0[:,k])
                mean = st.mean(x)
                means_0[k] = mean
                var = st.variance(x)
                vars_0[k] = var
        else:
            confusion_matrix[0][1]+=1
    
    

    print("Actual: " , y_test[i])
print("Accuracy: ",cr/20*100 , "%")
print(confusion_matrix)

