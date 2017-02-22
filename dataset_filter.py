from urllib2 import urlopen
import json
import time
import reverse_geocoder
import matplotlib.pyplot as plt

def getplaceonline(lat, lon):
    url = "http://maps.googleapis.com/maps/api/geocode/json?"
    url += "latlng=%s,%s&sensor=false" % (lat, lon)
    v = urlopen(url).read()
    j = json.loads(v)
    #print j
    try:
        components = j['results'][0]['address_components']
        #print components
    except:
        time.sleep(2)
    town = None
    for c in components:
        if "administrative_area_level_1" in c['types']:
            town = c['long_name']
    return town
    
def getplaceoffline(lat, lon):
    coordinates = list()
    coordinates.append((lat,lon))
    results = reverse_geocoder.search(coordinates, mode=1)
    results = results[0]
    return results['name']
    
def filter_data(location):
    city_list = ["New York City", "Washington, D.C.", "Philadelphia"]
    if location in city_list:
        return True
    return False

def get_corner_points(data_list):
    lat_list = list()
    lon_list = list()
    for checkIn in data_list:
        checkIn = checkIn.split()
        lat = checkIn[2]
        lon = checkIn[3]
        lat_list.append(float(lat))
        lon_list.append(float(lon))
    plt.plot(lon_list, lat_list, 'ro')
    plt.show()
    raw_input()
    
def filter_points(lat, lon):
    lat_t = 41.5
    lat_b = 37.9
    lon_l = -78
    lon_r = -73.23
    if not (lat>=lat_b and lat<=lat_t):
        return False
    if not (lon>=lon_l and lon<=lon_r):
        return False
    return True
      
def draw_graph(data_list, complete_list):
    lat_list_c = list()
    lon_list_c = list()
    #for checkIn in data_list:
    #    checkIn = checkIn.split()
    #    lat = checkIn[2]
    #    lon = checkIn[3]
    #    lat_list.append(float(lat))
    #    lon_list.append(float(lon))
    #print len(lat_list)
    #print "yo2"
    for checkIn in complete_list:
        checkIn = checkIn.split()
        lat = checkIn[2]
        lon = checkIn[3]
        lat_list_c.append(float(lat))
        lon_list_c.append(float(lon))
    #print "yo3"
    #fig = plt.figure(figsize=(8,6))

    #plt.plot(lon_list, lat_list, label='selected', lw=2, marker='o')
    #plt.plot(lon_list_c, lat_list_c, label='all', lw=2, marker='s')
    #plt.xlabel('longitude')
    #plt.ylabel('latitude')
    #plt.grid()
    #plt.legend(loc='upper right')

    #plt.gcf().autofmt_xdate()

    #plt.show()
    plt.plot(lon_list_c, lat_list_c, 'go')
    #plt.plot(lon_list, lat_list, 'ro')
    plt.show()
    raw_input()    
    
checkInDataset = open("Brightkite_totalCheckins.txt","r")
#checkInDataset = open("Gowalla_totalCheckins.txt","r")
count = 0
count2 = 0
state_count = dict()
state_user_count = dict()
location_id_map = dict()
user_id_set = set()
lon_arr = list()
filtered_data = list()
#location_id_set = set()
complete_list = list()
count3=0
plot_list = list()
filtered_dataset = open('Brightkite_filter_dataset.txt', 'w')
for checkIn_ele in checkInDataset:
    checkIn = checkIn_ele.split()
    try:
        user = checkIn[0]
        lat = checkIn[2]
        lon = checkIn[3]
        complete_list.append(checkIn_ele)
        lon_arr.append((lon, lat))
        location_id = checkIn[4]
        #print lat, lon
        if location_id in location_id_map:
            state = location_id_map[location_id]
        else:
            state = getplaceoffline(lat, lon)
            location_id_map[location_id] = state
        #if filter_data(state):
        #    filtered_data.append(checkIn_ele)
        if filter_points(float(lat), float(lon)):
            #plot_list.append(checkIn_ele)
            filtered_dataset.write(checkIn_ele)
            count3 = count3 + 1
            user_id_set.add(user)
         #print state_count
        #if state in state_count:
        #    state_count[state] = state_count[state] + 1
        #    user_set = state_user_count[state]
        #    user_set.add(user)
        #    state_user_count[state] = user_set
            #state_user_count[state] = state_user_count[state] + 1
        #else:
        #    state_count[state] = 1
        #    state_user_set = set()
        #    state_user_set.add(user)
        #    state_user_count[state] = state_user_set
    except:
        print "error"
        count2=count2+1
    count = count+1
    if count%100000==0:
        #print state_count
        print "hello"
        print count
filtered_dataset.close()
print "done"
print count3
checkInDataset.close()
#lon_arr.sort()
#print lon_arr
print "user count"
print len(user_id_set)
print "error data " + str(count2)

#get_corner_points(plot_list)
#draw_graph(filtered_data, complete_list)

#state_count = sorted(state_user_count.items(), key=lambda x: (-len(x[1]), x[0]))
#state_count = sorted(state_count.items(), key=lambda x: (-x[1], x[0]))
#f = open('gowalla_state_data_user1.txt', 'w')
#for ele in state_count:
#    f.write(str(ele[0]) + ": " + str(len(ele[1])) + "\n")
    #f.write(str(ele[0]) + ": " + str(ele[1]) + "\n")
#f.close()
#print "yeah yeah"
#
edge_list = open("Brightkite_edges.txt", "r")
edge_count = 0
for edge in edge_list:
    edge = edge.split()
    user1 = edge[0].strip()
    user2 = edge[1].strip()
    if user1 in user_id_set and user2 in user_id_set:
        edge_count = edge_count + 1
print "edge count"
print edge_count
edge_list.close()
