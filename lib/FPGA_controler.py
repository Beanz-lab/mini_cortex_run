import array
import serial

def init(env_args):
    global EVENT_ENABLE, MONITOR_ENABLE, MONITOR_PERIOD, FPGA_SER_PATH, PULSE_WIDTH, fpga_ser
    EVENT_ENABLE = env_args['EVENT_ENABLE']
    MONITOR_ENABLE = env_args['MONITOR_ENABLE']
    MONITOR_PERIOD = env_args['MONITOR_PERIOD']
    FPGA_SER_PATH = env_args['FPGA_SER_PATH']
    PULSE_WIDTH = 0x06 # env_args['PULSE_WIDTH']

    fpga_ser = serial.Serial(FPGA_SER_PATH,115200, timeout=0)

def tx_setup():
    tx_array = array('B',[]*200)

    # Defines the type of data the FPGA will output, monitor (23 bytes) or event mode (8 bytes)
    tx_array.append(MONITOR_ENABLE)
    tx_array.append(EVENT_ENABLE)

    tx_array.append(PULSE_WIDTH)
    tx_array.append(0xFF)
    tx_array.append(MONITOR_PERIOD)                 
    tx_array.append((0x0000FF00 & MONITOR_PERIOD)>>8)
    tx_array.append((0x00FF0000 & MONITOR_PERIOD)>>16)  
    tx_array.append((0xFF000000 & MONITOR_PERIOD)>>24)   

    fpga_ser.write(bytes(tx_array))


  
mon_array = array('f',[]*50)

def event_handler():
    rx_array = array('B',[]*500)
    data = fpga_ser.readline()
    for byte in data:
        rx_array.append(byte)

    # bitwise opperators '<<', '&', and '|' https://www.geeksforgeeks.org/python/python-bitwise-operators/
    # first byte
    header = ((rx_array[1] & 0x00ff) << 8) | (rx_array[0] & 0x00ff)
    # event mode trailer ends at byte 8, monitor mode trailer ends at byte 23
    event_tailer = ((rx_array[7] & 0x00ff) << 8) | (rx_array[6] & 0x00ff)
    monitor_trailer = ((rx_array[22] & 0x00ff) << 8) | (rx_array[21] & 0x00ff)

    if(header == 0xa5a5 and event_tailer == 0xd5d5):
        eve_word = ((rx_array[5] & 0x000000ff) << 24) | ((rx_array[4] & 0x000000ff) << 16) | ((rx_array[3] & 0x000000ff) << 8) | rx_array[2]
        return eve_word