import numpy as np 
books = np.array([])
bookDictionaries = []

bookTotalWords = []
# print("h")
bagOfWords = np.array([])


sum =0
# print("h")
for i in range(1,7):
    file = open("HP" + str(i) + ".txt")
    # print("h")
    books = np.append(books,file.read())
    words = books[i-1].split(" ")
    print("a")

    dictionary = {}
    numWords = 0
    # print("h")
    for word in words:
        numWords += 1
        # bagOfWords = np.append(bagOfWords,word)
        if word in dictionary:
            dictionary[word] += 1
        else:
            dictionary[word] = 1    
    sum += numWords
    # print("h")
    bookDictionaries.append(dictionary)
    bookTotalWords.append(numWords)

print(sum)
print(len(bagOfWords))