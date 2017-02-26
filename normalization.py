import time
import datetime
import calendar

def convertToTimestamp(timestring):
    #print timestring
    timestamp = calendar.timegm(time.strptime(timestring, '%Y-%m-%dT%H:%M:%SZ'))
    #print timestamp
    return timestamp
 
def normalize(ele_list):
    min_ele = min(ele_list)
    max_ele = max(ele_list)
    normalized_list = list()
    for ele in ele_list:
        ele = float(ele - min_ele)/float(max_ele-min_ele)
        normalized_list.append(ele)
    print normalized_list[:10]
    return normalized_list
    
def getNormalizedDuration(durationInSeconds):
	f = open('Brightkite_filter_dataset.txt', 'r')
	maxCheckin = -1
	minCheckin = 99999999999999999999999999999

	for entry in f:
		entryList = entry.split()
		timeStamp = convertToTimestamp(entryList[1].strip())
		if timeStamp > maxCheckin:
			maxCheckin = timeStamp
		if timeStamp < minCheckin:
			minCheckin = timeStamp
	f.close()

	return float(durationInSeconds)/(maxCheckin - minCheckin)
		

f = open('Brightkite_filter_dataset.txt', 'r')
lat_list = list()
lon_list = list()
time_list = list()
user_list = list()
loc_id_list = list()
for checkIn in f:
    checkIn = checkIn.split()
    user = int(checkIn[0])
    user_list.append(user)
    time_val = checkIn[1].strip()
    time_list.append(convertToTimestamp(time_val))
    lat = float(checkIn[2].strip())
    lat_list.append(lat)
    lon = float(checkIn[3].strip())
    lon_list.append(lon)
    loc_id = checkIn[4].strip()
    loc_id_list.append(loc_id)

time_list = normalize(time_list)
lat_list = normalize(lat_list)
lon_list = normalize(lon_list)

ind_list = [i[0] for i in sorted(enumerate(time_list), key=lambda x:x[1])]

f = open('Brightkite_normalized_filter_sorted_dataset1.txt', 'w')
print repr(lat_list[0])
for ind in ind_list:
    entry = str(user_list[ind]) + "  " + repr(time_list[ind]) + "  " + repr(lat_list[ind]) + "  " + repr(lon_list[ind]) + "  " + str(loc_id_list[ind]) + "\n"
    f.write(entry)
f.close()    
