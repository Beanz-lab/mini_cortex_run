# Mini CoRTEx - Run

## About Run

Run is a set of tools for iniializing and opperating the Mini CoRTEx

## About Mini CoRTEx

The mini Cosmic Ray Tracking Experiment (CoRTEx) is an experimental detector being built at the University of Pittsburgh with the goal of detecgin and displaying muon paths for education and outreach purposes.
Mini CoRTEx uses a 18 soild scintilator bars to organized to create a 3x3x3 detection grid. When a muon enters the detector energy is deposited in the scintilator bars which is detected by a silicon photo multiplier (SiPM).
Signals from the SiPM are monitored by a FPGA which preforms coincidence and sends positive detections to a Raspberry Pi 4b for data saving, detector monitoring, and live data display purposes.
The live data display uses a 3d LED cube to reconstruc the paths of the muons in real time as they are detected.
