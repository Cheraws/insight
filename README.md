# Insight Coding Challenge

# Running the Program

## Dependencies
Code done in python3. Run using run.sh

Python libraries: csv, time, datetime, collections, heapq, datetime
# Approach

## Data Structures
There are two main data structures.

The first data structure I use is an OrderedDict called userinfo. This holds active user session info. The key is the IP of the user, while the value contains a UserData object that represents the user's information. In this object, I keep track of the current time, the most recent time the user accessed something, and the number of requests that he has made.

The second data structure is another dictionary. The key is a date to represnt all the logs recorded at that date. The values contain a min heap that has all of the users that have logged on that day, and a set to make sure that there aren't dupe users in the bucket. In a way, each time slot is a bucket of sorts. 

## The Algorithm
Each request is read from the file in order. If the user isn't already in the userinfo dictionary, create the user session. If it is already there, change the users most recent access to current request time and increase the number of user document requests by 1. I add this value to a time bucket containing all the accesses made by any user at that time. After I insert the user's information, I make a check to see if any user sessions need to be timed out. There is a variable sessionWindowStart that is initialized to the very first access time of the EDGAR logs. This variable represents the left side of the session window and is always incrementing. I increment the sessionWindowStart until the sessionWindowStart plus the inactivity time is greater than the current time of the current request. For each bucket representing a time of access, I determine if a user is timed out. If the requests in the bucket have the same access time as the last request recorded  in the userinfo dictionary, I print the user's logging session and delete him from the active user session info dict. When a bucket’s heap is empty because I have processed all the requests, I delete the bucket. I can do this because I know the entries are in order of time. Once I reach the end of the file, I have to end all open sessions. I go through the user session info dict, printing all of the users that have not yet expired in the order that they accessed files.

## Different Solutions and Possible Constraints
If the printing order did not matter, a queue might be more suitable instead of a heap, given that insertion in a queue is much faster. In the case where there are very many accesses in a short period of time, a bucket could become particularly full. If there are more users than the max number possible, overflow issues might affect the ordering logic too. If I had access to a database, I could deal with many more users than with the current implementation.
# Directory Structure

    ├── README.md
    ├── run.sh
    ├── src
    │   └── sessionization.py
    ├── input
    │   └── inactivity_period.txt
    │   └── log.csv
    ├── output
    |   └── sessionization.txt
    ├── insight_testsuite
        └── run_tests.sh
        └── tests
            └── test_1
            |   ├── input
            |   │   └── inactivity_period.txt
            |   │   └── log.csv
            |   |__ output
            |   │   └── sessionization.txt

Various extra tests within the test folder.
