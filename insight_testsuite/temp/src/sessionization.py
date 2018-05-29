import csv
import sys
from pathlib import Path
import time
import datetime
import collections
import heapq
from queue import Queue
from datetime import timedelta 


class UserTime:
    def __init__(self, ip,requests,logs,current_time):
        self.ip = ip
        self.requests = requests
        self.logs = logs
        self.current_time = current_time

    def __lt__(self,other):
        return self.logs < other.logs
    


class UserData:
    total_logs = 0
    def __init__(self,current_time,requests,ip):
        self.logs = UserData.total_logs + 1
        UserData.total_logs = self.logs
        self.current_time = current_time
        self.end_time = current_time
        self.requests = requests
        self.ip = ip
    
    def __lt__(self, other):
        return self.logs < other.logs

def convertTime(log_date, log_time):
    f = "%Y-%m-%d %H:%M:%S"
    d_str = '{0} {1}'.format(log_date, log_time)
    time = datetime.datetime.strptime(d_str, f)
    return time

def checkInactiveHeap(time_heaps, old_time, user_info,inactivity_time,current_time,final=False):
    #Go through queue until the time gap is less than the inactivity timer.
    while old_time < current_time:
        if old_time + timedelta(seconds=inactivity_time) >= current_time:
            return old_time
        else:
            if old_time in time_heaps:
                while time_heaps[old_time]:
                    data = heapq.heappop(time_heaps[old_time])
                    ip = data.ip
                    #if maximum request one already filtered out.
                    if ip not in  user_info:
                        continue
                    if data.current_time == user_info[ip].end_time:
                        printUserData(user_info[ip],ip)
                        del(user_info[ip])
                #save time of old_time
                del time_heaps[old_time]
        old_time = old_time + timedelta(seconds=1)
    return old_time

def printUserData(user_data,ip):
    start_time = user_data.current_time
    end_time = user_data.end_time
    start_time_string = "{:%Y-%m-%d %H:%M:%S}".format(start_time)
    end_time_string = "{:%Y-%m-%d %H:%M:%S}".format(end_time)
    seconds = int((end_time - start_time).total_seconds() + 1)
    requests = user_data.requests
    return_text = ("{0},{1},{2},{3},{4}".format(ip, start_time_string,end_time_string,
        seconds, requests))
    print(return_text)
    with open(sys.argv[3],"a") as output_file:
        output_file.write(return_text + '\n')
            
    

    #Go through all the keys in order and finish printing up everything.
def checkNaiveInactive(user_times, inactivity_time,current_time,final=False):
    deleted_users = []
    for user in user_info.keys():
        if user_info[user].end_time + timedelta(seconds=inactivity_time) < current_time or final == True:
            printUserData(user_info[user],user)
            deleted_users += [user]
    for user in deleted_users:
        del(user_info[user])


if __name__ == "__main__":
    user_info = collections.OrderedDict()
    time_heaps = {}
    user_times = Queue()
    start = None
    inactivity_time = 2
    oldest_entry = None
    old_time = None
    logs = 0

    with open(sys.argv[3],"w") as output_file:
        print("clean file")

    with open(sys.argv[2],"r") as inactivity_time:
        inactivity_time = int(inactivity_time.read())

    #iterating through the input file.
    with open(sys.argv[1],"r") as input_file:
        reader = csv.DictReader(input_file, delimiter=",")
        header = reader.fieldnames
        for i, line in enumerate(reader):
            current_time = convertTime(line['date'], line['time'])
            if old_time == None:
                old_time = current_time
            #check to see if any files expired.
            old_time = checkInactiveHeap(time_heaps, old_time, user_info,inactivity_time,current_time)
            ip = line['ip']
            if ip not in user_info:
                user_data = UserData(current_time,  0, ip)
                user_info[ip] = user_data
            else:
                user_data = user_info[ip]
            user_data.requests += 1
            user_data.end_time = current_time
            #min heap to make sure files are outputted in start time order.
            details = UserTime(line['ip'], user_data.requests,user_info[ip].logs,current_time)
            if current_time not in time_heaps:
                time_heaps[current_time] = []
            heapq.heappush(time_heaps[current_time],details)
            user_times.put(details)
    checkNaiveInactive(user_times,inactivity_time, current_time,True)
    #checkInactivity(user_times, oldest_entry, user_info,inactivity_time,current_time, final="True")


            

            

