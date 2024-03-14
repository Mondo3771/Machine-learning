import numpy as np 
import math as math

books = np.array([])
bookDictionaries = []

bookTotalWords = []
sum = 0
bagOfWords = []

testPages = []

for i in range(1,8):
    file = open("HP" + str(i) + ".txt")

    books = np.append(books,file.read())

    pages = books[i-1].split("\n") # get the pages of the ith book

    testPages.append(pages[round(len(pages)*0.8):]) #last 20% of a book are reserved for testing.

    words = books[i-1].split(" ")
    
    size = len(words)
    wordsTraining = words[:round(size*0.8)] #first 80% of a book are reserved for testing
    # print(wordsTraining[0:10])

    dictionary = {} # initialise dictionary for each book
    numWords = 0

    for word in wordsTraining:
        if word == "":
            pass
        else:
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
bagOfWords = bagOfWords[1:]
bookPriors = []
# print("" in bookDictionaries[0])

for i in range(7):
    bookPriors.append(bookTotalWords[i] / sum)

# Create a vector based on bag   
#given a page create a vector based on the book    
def createVector (bag , page, dict):
    words = page.split(" ") # individual words in a page
    # words = list(set(words))
    words = words[1:]
    # print(len(words), " words")

    vector = np.zeros(len(bag)) 
    x = 0
    for word in words:
        if word in dict:
            x += 1
            vector[bag.index(word)] = 1        
    # print(x , " words found in book")
    return vector           


vectors = []
vectors.append(createVector(bagOfWords, pages[0], bookDictionaries[0]))
vectors.append(createVector(bagOfWords, pages[0], bookDictionaries[1]))
vectors.append(createVector(bagOfWords, pages[0], bookDictionaries[2]))
vectors.append(createVector(bagOfWords, pages[0], bookDictionaries[3]))
vectors.append(createVector(bagOfWords, pages[0], bookDictionaries[4]))
vectors.append(createVector(bagOfWords, pages[0], bookDictionaries[5]))
vectors.append(createVector(bagOfWords, pages[0], bookDictionaries[6]))

# print(pages[0])
# print(bagOfWords.index("chest;"))
# print(vectors[6][bagOfWords.index("chest;")])

# print(bookTotalWords)
# print(sum)
# print(bookPriors)

# now to calculate the probability 
def probabilitySentenceGivenBook(vector, bag ,  dict, totalWords):
    prob = 1
    for index in range(len(vector)):
        if vector[index] == 1:
            # print(prob)
            if bag[index] not in dict or dict[bag[index]] ==0 :
                prob +=   abs(math.log(1 / (totalWords + 2),10))
            else:  
                prob += abs(math.log(dict[bag[index]] / totalWords,10))
        else:
            # print(prob)
            if bag[index] not in dict or dict[bag[index]] ==0 :
                prob +=  abs(math.log( 1 - 1 / (totalWords + 2),10))
            else:    
                prob +=  abs( math.log(1 - dict[bag[index]] / totalWords,10))
    return prob

for i in range(7):
    probConditional = probabilitySentenceGivenBook(vectors[i],bagOfWords, bookDictionaries[i], bookTotalWords[i])
    

    probNumerator = probConditional + abs(math.log(bookPriors[i]))

    probDenominator = probConditional



    print(probNumerator)