# Mini CoRTEx - Run

## About Run

Run is a set of tools for initializing and opperating the Mini CoRTEx

## About Mini CoRTEx

The Mini Cosmic Ray Tracking Experiment (Mini CoRTEx) is an experimental detector being built at the University of Pittsburgh with the goal of detecting and displaying muon paths for education and outreach purposes.
Mini CoRTEx uses a 18 soild scintilator bars to organized to create a 3x3x3 detection grid. When a muon enters the detector energy is deposited in the scintilator bars which is detected by a silicon photo multiplier (SiPM).
Signals from the SiPMs are monitored by a Field-programable Gate Array (FPGA) which preforms coincidence checking and sends positive detections to a Raspberry Pi 4b for data saving, detector monitoring, and live data display purposes.
The live data display uses a 3d LED cube to reconstruct the paths of the muons in real time as they are detected.

# How to use Run

## Layout of Run

The root folder of run contains one a source directroy (src/), a run.sh script, and a default_init.json file. 

The **source directory** contains all of the code and modules necessary for interacting with the FPGA and LED Cube. Inside you will find the main file 'mini_cortext_run.py' as well as 'usr_start.py'. The later file is WIP and is intended to automate the creation of init.json files and to start run so there is a flexible enrty point into the program. 

The **run.sh** script simply sets the appropriate working dir, and calls 'mini_cortex_run.py' without any arguments. Passing no arguments means 'mini_cortex_run.py' will load the **default_init.json** file

The **default_init.json** file contains definitions for environment variables used throughout the program. This file is automatically loaded when 'mini_cortex_run.py' is executed without any arguments. You may load different init.json files if '-i' or '--init' is passed and a path to your custom init.json is provided.

## Starting Run

Currently there are 2 ways to start Run (plans for 3).

1. Run ./run.sh from your terminal to load default configuration. If this is not working ensure that run.sh is executable using 'chmod +x run.sh'.
2. Execute 'python3.7 src/mini_cortex_run.py'. This will also load default configs unless '-i' or '--init' and a path to a custom init.json are provided. Be sure to run this command from the root directory of mini_cortex_run
