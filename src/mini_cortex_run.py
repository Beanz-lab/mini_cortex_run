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

init_path = vars(parser.parse_args())

with open(init_path["init"]) as f:
    env_args = json.load(f)

print(f"loaded {init_path['init'].split('/')[-1]}")
EVENT_ENABLE = env_args["EVENT_ENABLE"]
MONITOR_ENABLE = env_args["MONITOR_ENABLE"]
MONITOR_PERIOD = env_args["MONITOR_PERIOD"]
FPGA_SER_PATH = env_args["FPGA_SER_PATH"]
PULSE_WIDTH = 0x06 # env_args["PULSE_WIDTH"]
TIME_STR = time.strftime("%Y-%m-%d_%H-%M-%S")

print(f"date_time: {TIME_STR}")
FPGA_controler.init(env_args)
FPGA_controler.tx_setup()


if EVENT_ENABLE == 1:
    os.makedirs("data/event/", exist_ok=True)
    event_data_file = open(f"data/event/{TIME_STR}.csv", "w")

    while True:
        event_data = FPGA_controler.event_handler()
        event_data_file.write(TIME_STR)
        event_data_file.write(" ")
        event_data_file.write(f"{event_data:032b}")
        event_data_file.write("\n")

        # send_LED_cube_animate(f"{eve_word:032b}", box_info=box_info, mapping=mapping, bit_low=bit_low, bit_high=bit_high)
        print ("Timestamp and Event",TIME_STR)   
        print(f"{event_data:032b}")





if MONITOR_ENABLE == 1:
    os.makedirs("data/monitor/", exist_ok=True)
    monitor_data_file = open(f"data/monitor/{TIME_STR}.csv", "w")

