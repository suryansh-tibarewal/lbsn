from constants import BRIGHTKITE_DATASET, GOWALLA_DATASET , buffer_time , rp
import user_checkin
from maths import eucledianDist

checkin_list = dict()

def initialize(dataset_type):
    global checkin_list
    checkin_list = user_checkin.user_checkin(dataset_type)

def get_pos(uid,time):
    global checkin_list
    speed = 0
    loc = [0,0]
    time_list = checkin_list[uid]
    if(time==time_list[0][0]):
        loc[0] = time_list[0][1]
        loc[1] = time_list[0][2]
        return loc
    for index,ti in enumerate(time_list[:-2]):
        t = ti[0]
        if(time==t):
            loc[0] = ti[1]
            loc[1] = ti[2]
            return loc
        elif(time>t and time_list[index+1][0]>time):
            time_gap = time_list[index+1][0]-t-buffer_time
            if(time_gap<=0):
                return [ti[1],ti[2]]
            speed = eucledianDist(time_list[index+1][1] , time_list[index+1][2] , time_list[index][1] , time_list[index][2])/time_gap
            loc[0] = speed*time*(time_list[index+1][1]-time_list[index][1]) + time_list[index][1]
            loc[1] = speed*time*(time_list[index+1][2]-time_list[index][2]) + time_list[index][2]
            return loc
    if(time_list[-1][0]==time):
        return [time_list[-1][1],time_list[-1][2]]
    return None

def neg(uid,t):
    u_loc = get_pos(uid,t)
    ans = []
    if(u_loc==None):
        return ans
    for user in checkin_list:
        if(user!=uid):
            v_loc = get_pos(user,t)
            if(v_loc!=None):
                if( eucledianDist(u_loc[0],u_loc[1],v_loc[0],v_loc[1]) <= rp):
                    ans.append(user)
    return ans

def usersInRegion(x,y,r,t):
    ans = []
    for user in checkin_list:
        v_loc = get_pos(user,t)
        if(v_loc!=None):
            if( eucledianDist(u_loc[0],u_loc[1],v_loc[0],v_loc[1]) <= r):
                ans.append(user)
    return ans
#print get_pos(0,.56065)
#print neg(0,0.600)
