#!/usr/bin/python3
# e.g. $ sudo python3 policyFetcher.py -p 2
import argparse
import locallib
#############################################################################
def parse_args():
    parser = argparse.ArgumentParser(description="Scheduler to check changes in kvstore.txt")
    parser.add_argument('-p', '--periodicity',  default=1, type=int, dest='timePeriod', help='Script periodicity in seconds')
    args = parser.parse_args()
    return args
#############################################################################
args=parse_args()
print("Log policyFetcher.py")
#print(args)
locallib.initilizer()
locallib.execute_update()
''' Periodic stub
while True:
    if os.path.exists(FILENAME):
        # Get the last modification time
        new_last_modified = os.path.getmtime(FILENAME)
        if last_modified is None:
            last_modified = new_last_modified
        elif new_last_modified != last_modified:
            print(f'File {FILENAME} has changed')
            execute_update()
            last_modified = new_last_modified
    time.sleep(args.timePeriod)  # Sleep for 1 second
'''