f = open('data_brightkite.txt', 'r')

recordList = []
for line in f:
	record = line.split(' ')
	recordList.append(record)

f.close()


