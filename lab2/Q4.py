import numpy as np 

books = np.array([])
bookDictionaries = []

bookTotalWords = []
sum = 0
bagOfWords = []

for i in range(1,8):
    file = open("HP" + str(i) + ".txt")

    books = np.append(books,file.read()) 
    words = books[i-1].split(" ")
    size = len(words)
    wordsTraining = words[:round(size*0.8)]
    
    # wordsTest = words[round(size*0.8):]

    dictionary = {}
    numWords = 0

    for word in wordsTraining:
        numWords += 1
        bagOfWords.append(word)
        if word in dictionary:
            dictionary[word] += 1
        else:
            dictionary[word] = 1    
    bookDictionaries.append(dictionary)
    bookTotalWords.append(numWords)
    sum += numWords

bagOfWords = list(set(bagOfWords))  # List of all the unique words in the books to make vectors

bookPriors = []

for i in range(7):
    bookPriors.append(bookTotalWords[i] / sum)
print(bookPriors)

