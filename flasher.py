import struct
import os
import sys
import glob
import serial.tools.list_ports
import serial

FLASH_HAL_OK = 0x00
FLASH_HAL_ERROR = 0x01
FLASH_HAL_BUSY = 0x02
FLASH_HAL_TIMEOUT = 0x03
FLASH_HAL_INV_ADDR = 0x04

# Bootloader Commands
COMMAND_BL_GET_VER = 0x51
COMMAND_BL_GET_HELP = 0x52
COMMAND_BL_GET_CID = 0x53
COMMAND_BL_GET_RDP_STATUS = 0x54
COMMAND_BL_GO_TO_ADDR = 0x55
COMMAND_BL_FLASH_ERASE = 0x56
COMMAND_BL_MEM_WRITE = 0x57
COMMAND_BL_EN_R_W_PROTECT = 0x58
COMMAND_BL_MEM_READ = 0x59
COMMAND_BL_READ_SECTOR_P_STATUS = 0x5A
COMMAND_BL_OTP_READ = 0x5B
COMMAND_BL_DIS_R_W_PROTECT = 0x5C

# lenght to follow  details of every command
COMMAND_BL_GET_VER_LEN = 6
COMMAND_BL_GET_HELP_LEN = 6
COMMAND_BL_GET_CID_LEN = 6
COMMAND_BL_GET_RDP_STATUS_LEN = 6
COMMAND_BL_GO_TO_ADDR_LEN = 10
COMMAND_BL_FLASH_ERASE_LEN = 8
COMMAND_BL_MEM_WRITE_LEN = 11
COMMAND_BL_EN_R_W_PROTECT_LEN = 8
COMMAND_BL_MEM_READ = 11
COMMAND_BL_READ_SECTOR_P_STATUS_LEN = 6
COMMAND_BL_OTP_READ_LEN = 8
COMMAND_BL_DIS_R_W_PROTECT_LEN = 6

verbose_mode = 1
mem_write_active =0

#-----------------------------------------------------------------------#
#------------------------ file operations ------------------------------#
#-----------------------------------------------------------------------#
def GetFileSize():
    size = os.path.getsize("stm32f4xx_application.hex")
    return size

def OpenFile():

    global HexFile
    HexFile = open('stm32f4xx_application.hex','rb')

def ReadFile():
    pass

def CloseFile():
    HexFile.close()


def GetSerialComPort():
    return serial.tools.list_ports.comports()

#---------------------------------------------------------------------#
#---------------------------- Utilities ------------------------------#
#---------------------------------------------------------------------#

def WordToByte(addr, index):
    value = (addr >> (8 * (index - 1)) & 0x000000FF)
    return value

def GetCrc(buffer, length):
    Crc = 0xFFFFFFFF

    #print(length)
    for data in buffer[0:length]:
        Crc = Crc ^ data
        for i in range(32):
            if(Crc & 0x80000000):
                Crc = (Crc << 1) ^ 0x04C11DB7
            else:
                Crc = (Crc << 1)
    return Crc


#---------------------------------------------------------------------#
#-------------------------- Serial Port ------------------------------#
#---------------------------------------------------------------------#

def SerialPorts():
    """ Lists serial port names
        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result


def SerialPortConfiguration(port):
    global ser
    try:
        ser = serial.Serial(port, 115200, timeout=2)
    except:
        print("\n   Oops! That was not a valid port")

        port = SerialPorts()
        if (not port):
            print("\n   No ports Detected")
        else:
            print("\n   Here are some available ports on your PC. Try Again!")
            print("\n   ", port)
        return -1
    if ser.is_open:
        print("\n   Port Open Success")
    else:
        print("\n   Port Open Failed")
    return 0


def ReadSerialPort(length):
    read_value = ser.read(length)
    return read_value


def CloseSerialPort():
    pass


def PurgeSerialPort():
    ser.reset_input_buffer()


def WriteToSerialPort(value, *length):
    data = struct.pack('>B', value)
    if (verbose_mode):
        value = bytearray(data)
        # print("   "+hex(value[0]), end='')
        print("   " + "0x{:02x}".format(value[0]), end=' ')
    if (mem_write_active and (not verbose_mode)):
        print("#", end=' ')
    ser.write(data)

#----------------------------------------------------------------------------------------#
#----------------------------- Command processing ---------------------------------------#
#----------------------------------------------------------------------------------------#

def ProcessCommandBootloaderGetVersion(length):
    bootloaderVersion = ReadSerialPort(1)
    value = bytearray(bootloaderVersion)
    print("\nBootloader Ver. : ", hex(value[0]))


def DecodeMenuCommandCode(command):
    ret_value = 0
    data_buf = []
    for i in range(255):
        data_buf.append(0)

    if (command == 0):
        print("\n   Exiting...!")
        raise SystemExit
    elif (command == 1):
        print("\n   Command == > BL_GET_VER")
        COMMAND_BL_GET_VER_LEN = 6
        data_buf[0] = COMMAND_BL_GET_VER_LEN - 1
        data_buf[1] = COMMAND_BL_GET_VER
        crc32 = GetCrc(data_buf, COMMAND_BL_GET_VER_LEN - 4)
        crc32 = crc32 & 0xffffffff
        data_buf[2] = WordToByte(crc32, 1, 1)
        data_buf[3] = WordToByte(crc32, 2, 1)
        data_buf[4] = WordToByte(crc32, 3, 1)
        data_buf[5] = WordToByte(crc32, 4, 1)

        WriteToSerialPort(data_buf[0], 1)
        for i in data_buf[1:COMMAND_BL_GET_VER_LEN]:
            WriteToSerialPort(i, COMMAND_BL_GET_VER_LEN - 1)

        ret_value = ReadbootloaderReply(data_buf[1])

    else:
        print("\n   Please input valid command code\n")
        return

    if ret_value == -2:
        print("\n   TimeOut : No response from the bootloader")
        print("\n   Reset the board and Try Again !")
        return


def ReadbootloaderReply(command_code):
    # ack=[0,0]
    len_to_follow = 0
    ret = -2

    # read_serial_port(ack,2)
    # ack = ser.read(2)
    ack = ReadSerialPort(2)
    if (len(ack)):
        a_array = bytearray(ack)
        # print("read uart:",ack)
        if (a_array[0] == 0xA5):
            # CRC of last command was good .. received ACK and "len to follow"
            len_to_follow = a_array[1]
            print("\n   CRC : SUCCESS Len :", len_to_follow)
            # print("command_code:",hex(command_code))
            if (command_code) == COMMAND_BL_GET_VER:
                ProcessCommandBootloaderGetVersion(len_to_follow)
            else:
                print("\n   Invalid command code\n")
            ret = 0

        elif (a_array[0] == 0x7F):
            # CRC of last command was bad .. received NACK
            print("\n   CRC: FAIL \n")
            ret = -1
    else:
        print("\n   Timeout : Bootloader not responding")

    return ret
