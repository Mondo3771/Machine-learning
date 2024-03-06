import numpy as np
# def laplace(s, count, county):
#     return (count + 1)/(county + 2)

# def no_laplace():


file1 = open("simple-food-reviews.txt")
words = file1.readline()[:-1] 
reviews = np.array([])
while len(words) != 0:
    reviews = np.append(reviews,words)
    words = file1.readline()[:-1]
np.random.shuffle(reviews)
#print(reviews)
# bag= np.array()
# for i in range(0,len( reviews)-1):
#     rev = reviews[i].split(" ")

# print (rev)
countp=0
countn=0

bags=np.array([])
dictP={}
dictN={}


for i in range(12):

    a=reviews[i].split()[1:]

    bags=np.append(bags,a)
    
    if reviews[i][0]=='1':
        countp+=1
        for j in a:
            # print(dictP[j])
            if j not in dictP:
                dictP.update({j:1})
            else:
                dictP.update({j:dictP[j]+1})    
    else:
      
        for k in a:
            # print(k not in dictN)
            if k not in dictN:
                dictN.update({k:1})
            else:
                dictN.update({k:dictN[k]+1}) 
        countn+=1
# print(dictP)
# print(dictN)

for k in dictP:
    dictP.update({k:dictP[k]/countp})

for k in dictN:
    dictN.update({k:dictN[k]/countn})

print(np.unique(bags))
print(dictP)
print(dictN)

priorP=countp/(countp+countn)
priorN=countn/(countp+countn)




