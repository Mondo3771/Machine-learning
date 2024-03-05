import numpy as np

file1 = open("simple-food-reviews.txt")
words = file1.readline()
reviews = np.array([]) 
reviews = np.append(reviews,words)

while len(words) != 0:
    words = file1.readline()
    reviews = np.append(reviews,words)

print(reviews)
