
######################		CONSTANTS		##############

n_users = 100
checkin_list = [ [0.500,3,0.5,0] , [0.594,1,0.2,0] , [0.423,2,0.45,0] , [0.3,1,0.2,0]]    ## Each element is [time,uid,location,status]
influenced_bits = [0,0,0,0,0,0,0,0,0,0,0]
Ti = [0,0,0,0,0,0,0,0,0,0,0]
i_list = [0]
matrix = []




######################		FUCNTIONS		######################
def getKey(item):
    return item[0]

def social_check(e , influenced):
	return True

def physical_check(e , influenced):
	return True

def check(e):
	res = 0
	for influenced in i_list:
		res = ( social_check(e , influenced)  | physical_check(e , influenced) )
		if res!=0:
			return 1;
	return 0;

def traverse():
	val = []
	for e in checkin_list:
		if ( e[3]==0 and influenced_bits[e[1]]==0 ):
			print(e[1],':',e[0])
			if check(e):
				val = e
				influenced_bits[e[1]]=1
				Ti[e[1]] = e[0]
				i_list.append(e[1])
				e[3]=1
				#print(val)
				return val
	return None






######################		EXE		#######################

checkin_list.sort()
#print(checkin_list)

for i in range(0,n_users):
	influenced_bits.append(0)

new_influenced = traverse()

while new_influenced!=None:
	new_influenced = traverse()

for i in i_list:
	print(str(i) , ':' , Ti[i])




