# checkIn list
# 0: userId INT
# 1: timestamp FLOAT (from 0 to 1)
# 2: latitude FLOAT (from 0 to 1)
# 3: longitude FLOAT (from 0 to 1)
# 4: location_id STRING
# 5: validity_status BOOLEAN

def getCheckInList(dataset_type):
    checkIn_object_list = list()
    if dataset_type == 0:
        checkInList = open('Brightkite_normalized_filter_sorted_dataset1.txt', 'r')
    else:
        checkInList = open('Gowalla_normalized_filter_sorted_dataset1.txt', 'r')
    for checkIn in checkInList:
        checkIn_entry = checkIn.split()
        checkInX = list()
        checkInX.append(int(checkIn_entry[0].strip()))
        checkInX.append(float(checkIn_entry[1].strip()))
        checkInX.append(float(checkIn_entry[2].strip()))
        checkInX.append(float(checkIn_entry[3].strip()))
        checkInX.append(str(checkIn_entry[4].strip()))
        checkInX.append(0)
        checkIn_object_list.append(checkInX)
    checkInList.close()
    return checkIn_object_list