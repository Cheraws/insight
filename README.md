# Insight Coding Challenge

# Approach

## Data Structures
I have two structures that I primarily use to solve this problem.

The first data structure I use is an OrderedDict called userinfo. The key is the IP of the user, while the value contains a UserData object
that represents the user's information. In this object, I keep track of the current time, the most recent time the user accessed something, 
and the number of requests that he has made.

The second data structure I use is a dictionary called time heaps. The key of the dictionary is the time of access. The value contains a heap that 
represents all accesses made by all users within that timeframe. The heap is sorted by when the user has first accessed the file to account for the case
where users are printed in order by first time access as a tiebreaker. 

## The Algorithm
Each request is read one after the other. If the request isn't already in the userinfo dictionary, add the request to it. If it is already in there, change the 
most recent access to that time and increase the number of requests by 1. We add this value to a time bucket containing all the accesses made by any user at that time. After we insert the first user's information, we make a check in the second data structure. There is a variable sessionWindowStart that is initialized as the very first access time of EDGAR. We increment the sessionWindowStart until the sessionWindowStart plus the inactivity time is greater than the current time of the current request. In each bucket represnting a time, we compare the logs in there with the userinfo dictionary. If the logs in the bucket have the same ending time as the data in the userinfo dictionary, we print the user's logging info and delete him from user info.

Once we reach the end of the file, we have to print all of the files. We go through the userinfo dictionary, printing all of the users that have not yet expired in the order that they accessed files. 


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
