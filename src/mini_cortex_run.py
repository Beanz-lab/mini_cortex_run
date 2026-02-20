import serial 
import json
import argparse
import time
import datetime
from array import *
import numpy as np

# We parse comand line arguments. If mini_cortext.py is executed directly from
# the comand line, default_init.json will be loaded. If -i is provided with a
# path to an init.json file, that file's contents will be read into the program
#
# These json files provide environment variable that are used for setup and 
# throughout the program.
parser = argparse.ArgumentParser()
parser.add_argument(
    "-i", "--init", 
    action="store", 
    default="default_init.json"
)

init_path = vars(parser.parse_args())

with open(init_path["init"]) as f:
    env_args = json.load(f)

print(f"loaded {init_path['init'].split('/')[-1]}")
EVENT_ENABLE = env_args["EVENT_ENABLE"]
MONITOR_ENABLE = env_args["MONITOR_ENABLE"]
MONITOR_PERIOD = env_args["MONITOR_PERIOD"]
FPGA_SER_PATH = env_args["FPGA_SER_PATH"]
PULSE_WIDTH = 0X06 # env_args["PULSE_WIDTH"]

timestr = time.strftime("%Y-%m-%d_%H-%M-%S")
print(f"date_time: {timestr}")

if EVENT_ENABLE == 1:
    event_data_file = open(f"data/event/{timestr}.csv")
