import numpy as np
def prob(v , d, b, cp):
    p=1
    # print(d)
    # print(v)
    for i in range(0,len(v)):
        if i == 1 and b[i] in d:
            p = p*d[b[i]]
            # print(d[b[i]])
        elif b[i]  in d:
            p=p*(1-d[b[i]])
    #         print(d[b[i]])
    #     print(p)
    #     print(b[i])
    #     print("]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]")
    # print("done")
    return p


file1 = open("simple-food-reviews.txt")
words = file1.readline()[:-1] 
reviews = np.array([])
while len(words) != 0:
    reviews = np.append(reviews,words)
    words = file1.readline()[:-1]
np.random.shuffle(reviews)
countp=0
countn=0

bags=np.array([])
dictP={}
dictN={}

for i in range(12):
    a=np.array(reviews[i].split()[1:])
    a= np.unique(a)
    bags=np.append(bags,a)
    
    if reviews[i][0]=='1':
        countp+=1
        for j in a:
            if j not in dictP:
                dictP.update({j:1})
            else:
                dictP.update({j:dictP[j]+1})    
    else:
        for k in a:
            if k not in dictN:
                dictN.update({k:1})
            else:
                dictN.update({k:dictN[k]+1}) 
        countn+=1
print(dictN)
print(dictP)
for k in dictP:
    dictP.update({k:dictP[k]/countp})

for k in dictN:
    dictN.update({k:dictN[k]/countn})
# print(bags)
bags= np.unique(bags)
priorP=countp/(countp+countn)
priorN=countn/(countp+countn)
for j in range(12,13):
    words = reviews[j]
    rev= words.split(" ")
    # print(bags)
    # print('h')
    # print(rev)
    vec = np.zeros(len(bags))
    # print(rev[1])
    # an = np.where(bags == rev[1])
    # print(len(an[0]))
    # print(an[0])
    lap ={}
    for i in range(1,len(rev)):
        # print(rev[i])
        an = np.where(bags == rev[i])[0]
        if len(an) ==0:
            print("hello")
        else:
            for k in an:
                vec[k]+=1
    # print(vec)
    # print(dictP)
    # print(bags)
                
    npr= prob(vec, dictN, bags,countn)
    pp= prob(vec, dictP,bags,countp )
    print(pp)
    print(npr)
    print(words)
    print(npr)
    print(']]]]]]]]]]]]]]]]]]]]]]]]]]]')
    print(pp)
    print(words)
    print(priorP*pp)
    print(priorN*npr)
    p= (priorN*npr)/(priorN*npr + priorP*pp)
    print(p)



