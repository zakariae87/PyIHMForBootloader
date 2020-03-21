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

#---------------------------------------------------------------------#
#------------------------file operations------------------------------#
#---------------------------------------------------------------------#
def GetFileSize():
    size = os.path.getsize("stm32f4xx_application.hex")
    return size

def OpenFile():
    global HexFile
    HexFile = open('stm32f4xx_application.hex','rb')
def ReadFile():
    pass


def GetSerialComPort():
    return serial.tools.list_ports.comports()


def OnSelectComPort(event=None):
    # get selection from event
    print("event.widget:", event.widget.get())
    # or get selection directly from combobox
    # print("comboboxes: ", combobox1.get())
