def user_checkin(dataset_type):
    if dataset_type == 0:
        checkInList = open('Brightkite_normalized_filter_sorted_dataset1.txt', 'r')
    else:
        checkInList = open('Gowalla_normalized_filter_sorted_dataset1.txt', 'r')
    user_list = dict()
    for checkIn in checkInList:
        checkIn_entry = checkIn.split()
        uid = int(checkIn_entry[0].strip())
        time = float(checkIn_entry[1].strip())
        xloc = float(checkIn_entry[3].strip())
        yloc = float(checkIn_entry[2].strip())
        if(uid not in user_list):
            user_list.update({uid:[[time,xloc,yloc]]})
        else:
            temp = user_list[uid]
            temp.append([time,xloc,yloc])
            user_list.update({uid:temp})
    checkInList.close()
    return user_list
