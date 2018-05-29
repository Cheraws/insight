import csv
import sys
from pathlib import Path
import time
import datetime
import collections
import heapq
from queue import Queue
from datetime import timedelta

# Data sturture that is stored inside a minheap. Contains the ip,
# requests, and the order it was accessed in.


class UserTime:
    def __init__(self, ip, logs):
        self.ip = ip
        self.logs = logs

    def __lt__(self, other):
        return self.logs < other.logs

# metadata of the user. Contains current_time, requests, and the IP of the
# user.


class UserData:
    total_logs = 0

    def __init__(self, current_time, requests, ip):
        self.logs = UserData.total_logs + 1
        UserData.total_logs = self.logs
        self.current_time = current_time
        self.end_time = current_time
        self.requests = requests
        self.ip = ip

    def __lt__(self, other):
        return self.logs < other.logs

# time conversion to a form that Python can utilize.


def convertTime(log_date, log_time):
    f = "%Y-%m-%d %H:%M:%S"
    d_str = '{0} {1}'.format(log_date, log_time)
    time = datetime.datetime.strptime(d_str, f)
    return time


def advanceSessionWindow(
        time_heaps,
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
            if session_window_start in time_heaps:
                while time_heaps[session_window_start][0]:
                    data = heapq.heappop(time_heaps[session_window_start][0])
                    ip = data.ip
                    # if maximum request one already filtered out.
                    if ip not in user_info:
                        continue
                    if session_window_start == user_info[ip].end_time:
                        printUserData(user_info[ip], ip)
                        del(user_info[ip])
                # save time of session_window_start
                del time_heaps[session_window_start]
        session_window_start = session_window_start + timedelta(seconds=1)
    return session_window_start

# outputs userdata to the file location given.


def printUserData(user_data, ip):
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

# Go through all the keys in order in the OrderedDict of users and finish
# printing up everything.

def checkNaiveInactive(user_times, inactivity_time, current_time, final=False):
    deleted_users = []
    for user in user_info.keys():
        if user_info[user].end_time + \
                timedelta(seconds=inactivity_time) < current_time or final:
            printUserData(user_info[user], user)
            deleted_users += [user]
    for user in deleted_users:
        del(user_info[user])


if __name__ == "__main__":
    user_info = collections.OrderedDict()
    time_heaps = {}
    start = None
    inactivity_time = None
    oldest_entry = None
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
            current_time = convertTime(line['date'], line['time'])
            if session_window_start is None:
                session_window_start = current_time
            # check to see if any files expired.
            session_window_start = advanceSessionWindow(
                time_heaps, session_window_start, user_info, inactivity_time, current_time)
            ip = line['ip']
            if ip not in user_info:
                user_data = UserData(current_time, 0, ip)
                user_info[ip] = user_data
            else:
                user_data = user_info[ip]
            user_data.requests += 1
            user_data.end_time = current_time
            # min heap to make sure files are outputted in start time order.
            details = UserTime(
                line['ip'],
                user_info[ip].logs)
            if current_time not in time_heaps:
                time_heaps[current_time] = ([], set())
            if ip not in time_heaps[current_time][1]:
                heapq.heappush(time_heaps[current_time][0], details)
                time_heaps[current_time][1].add(ip)
    checkNaiveInactive(user_info, inactivity_time, current_time, True)
    input_file.close()
