from random import choice

f = open('interest.txt', 'r')
interestList = f.read().split(',')
for inter in interestList:
	inter = inter.strip()

print len(interestList)
f.close()

userCount = 100
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
