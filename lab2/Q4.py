import numpy as np 

books = np.array([])
bookDictionaries = []

bookTotalWords = []
bagOfWords = []

for i in range(1,7):
    file = open("HP" + str(i) + ".txt")

    books = np.append(books,file.read())
    words = books[i-1].split(" ")

    dictionary = {}
    numWords = 0

    for word in words:
        numWords += 1
        bagOfWords.append(word)
        if word in dictionary:
            dictionary[word] += 1
        else:
            dictionary[word] = 1    
    bookDictionaries.append(dictionary)
    bookTotalWords.append(numWords)

bagOfWords = list(set(bagOfWords))    #List of all the unique words in the books to make vectors

print(bagOfWords)