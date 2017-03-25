from random import choice

f = open('interest.txt', 'r')
interestList = f.read().split(',')
s = list()
print type(interestList)
#for inter in interestList:
 #   print inter
  #  inter = inter.strip()
   # print inter
    #s.append(inter)
list1 = [1,1,1,1,1,1,1,1,1,1,1,1,1,1];
for i in list1:
    i +=10
print list1
#for 
print interestList
print s
print len(interestList)
f.close()

userCount = 10
res = []
for i in range(userCount):
	r = choice(range(0, 6, 1))
	userInterestSet = set()
	while r>0:
		flag = True
		while flag:
			userInterest = choice(interestList)
			if userInterest not in userInterestSet:
				flag = False
		userInterestSet.add(userInterest)
		r = r - 1
	res.append(userInterestSet)
    
print res
    
d = {}
d[0] = 0
d[1] = 0
d[2] = 0
d[3] = 0
d[4] = 0
d[5] = 0

for ent in res:
	d[len(ent)]+=1

for e in d:
	print d[e]	
