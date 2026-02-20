# import the main file to access env variables
import array
import mini_cortex_run as mcr

def tx_setup():
    tx_array = array('B',[]*200)

    # Defines the type of data the FPGA will output, monitor (23 bytes) or event mode (8 bytes)
    tx_array.append(mcr.MONITOR_ENABLE)
    tx_array.append(mcr.EVENT_ENABLE)

    tx_array.append(mcr.PULSE_WIDTH)
    tx_array.append(0xFF)
    tx_array.append(0x000000FF & mcr.MONITOR_PERIOD)                 
    tx_array.append((0x0000FF00 & mcr.MONITOR_PERIOD)>>8)
    tx_array.append((0x00FF0000 & mcr.MONITOR_PERIOD)>>16)  
    tx_array.append((0xFF000000 & mcr.MONITOR_PERIOD)>>24)   

    mcr.fpga_ser.write(bytes(tx_array))


  
mon_array = array('f',[]*50)

def event_handler():
    rx_array = array('B',[]*500)
    data = mcr.fpga_ser.readline()
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