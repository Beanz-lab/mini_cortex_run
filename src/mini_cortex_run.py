from lib import FPGA_controler
import json
import argparse
import time
import os

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

args = vars(parser.parse_args())

with open(args["init"]) as f:
    env_args = json.load(f)

# Set env variables
EVENT_ENABLE = env_args["EVENT_ENABLE"]
MONITOR_ENABLE = env_args["MONITOR_ENABLE"]
TIME_STR = time.strftime("%Y-%m-%d_%H-%M-%S")

print(f"Date_Time: {TIME_STR}")
print(f"Loaded {args['init'].split('/')[-1]}")
print(env_args)

# Pass env varibales to the FPGA_controler script and send setup to the FPGA
FPGA_controler.init(env_args)
FPGA_controler.tx_setup()
print("Setup sent to FPGA...")


# Event mode body. data is save from the FPGA, currently 32 bits are returned,
# im not sure why but thats how it is in mdaq_v2.py and mdaq_startup_v2.py. 
# Should return pixel data from the FPGA which would be 27 bits for 3x3x3 
# detector.
#
# Creates the data file to save data for archiving. Continualy querries the
# FPGA
if EVENT_ENABLE == 1:
    os.makedirs("data/event/", exist_ok=True)
    event_data_file = open(f"data/event/{TIME_STR}.txt", "w")

    print("Starting event mode!\n\n")
    while True:
        event_data = FPGA_controler.event_handler()
        event_data_file.write(TIME_STR)
        event_data_file.write(" ")
        event_data_file.write(f"{event_data:032b}")
        event_data_file.write("\n")

        # send_LED_cube_animate(
        #   f"{eve_word:032b}", 
        #   box_info=box_info, 
        #   mapping=mapping, 
        #   bit_low=bit_low, 
        #   bit_high=bit_high
        # )

        current_time = time.strftime("%H-%M-%S")
        print ("Timestamp and Event",current_time)   
        print(f"{event_data:032b}")



if MONITOR_ENABLE == 1:
    os.makedirs("data/monitor/", exist_ok=True)
    monitor_data_file = open(f"data/monitor/{TIME_STR}.csv", "w")

