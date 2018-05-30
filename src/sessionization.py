import csv
import sys
from pathlib import Path
import time
import datetime
import collections
import heapq
from queue import Queue
from datetime import timedelta

'''
metadata of the user. Contains current_time, requests, and the IP of the
 user.
'''

class UserData:
    total_index = 0

    def __init__(self, current_time, requests, ip):
        self.request_index = UserData.total_index + 1
        UserData.total_index = self.request_index
        self.current_time = current_time
        self.end_time = current_time
        self.requests = requests
        self.ip = ip

    def __lt__(self, other):
        return self.request_index < other.request_index

'''
time conversion to a form that Python can utilize.
'''

def convert_time(log_date, log_time):
    f = "%Y-%m-%d %H:%M:%S"
    d_str = '{0} {1}'.format(log_date, log_time)
    time = datetime.datetime.strptime(d_str, f)
    return time


'''
Advance with a window until the window is too big for the users to expire. In each bucket,
check to see if the users in the bucket have the same time as their own data. If they are, print to file.
'''
def advance_session_window(
        time_buckets,
        session_window_start,
        user_info,
        inactivity_time,
        current_time,
        final=False):
    # Go through queue until the time gap is less than the inactivity timer.
    while session_window_start < current_time:
        if session_window_start + timedelta(seconds=inactivity_time) >= current_time:
            return session_window_start
        else:
            if session_window_start in time_buckets:
                while time_buckets[session_window_start][0]:
                    ip = heapq.heappop(time_buckets[session_window_start][0])[1]
                    # if maximum request one already filtered out.
                    if ip not in user_info:
                        continue
                    if session_window_start == user_info[ip].end_time:
                        print_user_data(user_info[ip], ip)
                        del(user_info[ip])
                # save time of session_window_start
                del time_buckets[session_window_start]
        session_window_start = session_window_start + timedelta(seconds=1)
    return session_window_start

'''
outputs userdata to the file location given.
'''

def print_user_data(user_data, ip):
    start_time = user_data.current_time
    end_time = user_data.end_time
    start_time_string = "{:%Y-%m-%d %H:%M:%S}".format(start_time)
    end_time_string = "{:%Y-%m-%d %H:%M:%S}".format(end_time)
    seconds = int((end_time - start_time).total_seconds() + 1)
    requests = user_data.requests
    return_text = (
        "{0},{1},{2},{3},{4}".format(
            ip,
            start_time_string,
            end_time_string,
            seconds,
            requests))
    # print(return_text)
    with open(sys.argv[3], "a") as output_file:
        output_file.write(return_text + '\n')
        output_file.close()

'''
Go through all the keys in order in the OrderedDict of users and finish
 printing up everything.
'''

def finish_printing(user_info):
    deleted_users = []
    for user in user_info.keys():
        print_user_data(user_info[user], user)
        deleted_users += [user]
    for user in deleted_users:
        del(user_info[user])


def process_file():
    user_info = collections.OrderedDict()
    time_buckets = {}
    inactivity_time = None
    session_window_start = None
    logs = 0

    with open(sys.argv[3], "w") as output_file:
        print("clean file")

    with open(sys.argv[2], "r") as inactivity_time_file:
        inactivity_time = int(inactivity_time_file.read())
        inactivity_time_file.close()

    # iterating through the input file.
    with open(sys.argv[1], "r") as input_file:
        reader = csv.DictReader(input_file, delimiter=",")
        header = reader.fieldnames
        for i, line in enumerate(reader):
            current_time = convert_time(line['date'], line['time'])
            if session_window_start is None:
                session_window_start = current_time
            # check to see if any files expired.
            session_window_start = advance_session_window(
                time_buckets, session_window_start, user_info, inactivity_time, current_time)
            ip = line['ip']
            if ip not in user_info:
                user_data = UserData(current_time, 0, ip)
                user_info[ip] = user_data
            else:
                user_data = user_info[ip]
            user_data.requests += 1
            user_data.end_time = current_time
            # min heap to make sure files are outputted in start time order.

            if current_time not in time_buckets:
                time_buckets[current_time] = ([], set())
            if ip not in time_buckets[current_time][1]:
                heapq.heappush(time_buckets[current_time][0], (user_data.request_index,ip))
                time_buckets[current_time][1].add(ip)
    finish_printing(user_info)
    input_file.close()


if __name__ == "__main__":
    process_file()
    
