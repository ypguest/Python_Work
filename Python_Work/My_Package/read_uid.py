#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
sys.path.append(r'C:\Users\yinpeng\Desktop\WorkSpace\mygui\package_work')
from data_convert import *


# 输入uid_code, 得到lot_num, wafer_num, pol, x_pos, y_pos
# '3F 90 84 57 D2 49 00 90 FF 00 FF 00 FF 00 FF 00 C0 6F 7B A8 2D B6 FF 6F 00 FF 00 FF 00 FF 00 FF'  # old
# '0E 06 74 79 49 11 05 80 FF 00 FF 00 FF 00 FF 00 F1 F9 8B 86 B6 EE FA 7F 00 FF 00 FF 00 FF 00 FF'  # new
def uid_to_info(uid):
    charDecode = {'0': '0', '1': '1', '2': '2', '3': '3', '4': '4', '5': '5', '6': '6', '7': '7', '8': '8', '9': '9',
                  '10': '1', '11': 'B', '12': 'G', '13': 'H', '14': 'J', '15': 'M', '16': 'C', '17': 'D'}
    xSeqDecode = {'0': '0', '1': '1', '2': '2', '3': '3', '4': '4', '5': '5', '6': '6', '7': '7', '8': '8', '9': '9',
                  '10': 'A', '11': 'B', '12': 'C', '13': 'D', '14': 'E', '15': 'F', '16': 'G', '17': 'H', '18': 'J',
                  '19': 'K', '20': 'L', '21': 'M', '22': 'N', '23': 'P', '24': 'Q', '25': 'R', '26': 'S', '27': 'T',
                  '28': 'U', '29': 'V', '30': 'W', '31': 'X'}
    uid = bytes().fromhex(uid)            # 将16进制字符串转字节串
    fid_format = (uid[5] & 0x08) >> 3          # 0 为新format, 1为旧format
    if fid_format == 1:
        lot_number_u = (((uid[2] & 0x7F) << 16) | (uid[1]) << 8 | (uid[0] & 0xF8)) >> 3
        fab_encode = (uid[6] & 0x18) >> 3      # 0000,0000 & 0001,1000(右移3位) -> 0000，0000
        lot_number_l = (uid[7] & 0x80) >> 4 | uid[0] & 0x07     # 1001,0000 & 1000,0000 (右移4位 -> 1000) | 0111,1111 & 0000,0111 -> 1111(15)
        if lot_number_l == 0xB:   # 1011
            if fab_encode == 0x0:
                lot_number_l = 0xB      # 1011(11)
            elif fab_encode == 0x1:
                lot_number_l = 0x10     # 1000(8)
            elif fab_encode == 0x2:
                lot_number_l = 0x11     # 1001(17)
        lot_number_l = charDecode[str(lot_number_l)]

        lot_num = "{:06d}".format(lot_number_u) + lot_number_l   # 037383M
        wafer_num = ((uid[3] & 0x0F) << 1) | ((uid[2] & 0x80) >> 7)
        pol = ((uid[4] & 0x08) >> 3)
        x_pos = ((uid[4] & 0x07) << 3) | ((uid[3] & 0xE0) >> 5)
        y_pos = ((uid[5] & 0x07) << 4) | ((uid[4] & 0xF0) >> 4)

    elif fid_format == 0:

        lot_number_x0 = (uid[2] & 0x03) << 3 | (uid[1] & 0xE0) >> 5
        lot_number_x1 = (uid[1] & 0x1F)
        lot_number_x2 = (uid[0] & 0xF8) >> 3

        lot_number_x0 = xSeqDecode[str(lot_number_x0)]
        lot_number_x1 = xSeqDecode[str(lot_number_x1)]
        lot_number_x2 = xSeqDecode[str(lot_number_x2)]
        lot_year = (uid[3] & 0x0F)
        lot_work_week = (uid[2] & 0xFC) >> 2

        fab_encode = (uid[6] & 0x18) >> 3    # 0000,0101(05) & 0001,1000 -> 0000,0000
        lot_number_l = (uid[7] & 0x80) >> 4 | uid[0] & 0x07   # 1000,0000(80) & 1000,0000(80) -> 1000 | 1110 & 0111 -> 0110  => 1110
        if lot_number_l == 0xB:    # 1011
            if fab_encode == 0x0:
                lot_number_l = 0xB    # 1011
            elif fab_encode == 0x1:
                lot_number_l = 0x10
            elif fab_encode == 0x2:
                lot_number_l = 0x11
        lot_number_l = charDecode[str(lot_number_l)]
        if lot_number_l == 'J':
            lot_num = 'K' + str(lot_year) + '{:02d}'.format(lot_work_week) + lot_number_x0 + lot_number_x1 + lot_number_x2 + '0'
        else:
            lot_num = str(lot_year) + '{:02d}'.format(lot_work_week) + lot_number_x0 + lot_number_x1 + lot_number_x2 + lot_number_l
        wafer_num = ((uid[5] & 0x01) << 4) | ((uid[4] & 0xF0) >> 4)
        pol = ((uid[4] & 0x08) >> 3)
        x_pos = ((uid[4] & 0x07) << 3) | ((uid[3] & 0xE0) >> 5)
        y_pos = ((uid[6] & 0x03) << 4) | ((uid[5] & 0xF0) >> 4)
    return lot_num, wafer_num, pol, x_pos, y_pos


def efuse_to_info(Efuse_id):
    Efuse_id = Efuse_id.split('_')
    bin_id = ''
    for i in range(len(Efuse_id)):
        bin_id = hex2bin(Efuse_id[i][2:]) + bin_id  # 将Efuse_id转为0001100110010000000010010000000000101000100010010111001000000000
    Lot_ID = 'P' + lot_cov(bin_id[:30])
    Fab_ID = bin2dec(bin_id[30:31])
    Wafer_ID = bin2dec(bin_id[33:37])
    Die_X = bin2dec(bin_id[38:46])
    Die_Y = bin2dec(bin_id[47:55])
    return [Fab_ID, Lot_ID, Wafer_ID, Die_X, Die_Y]


if __name__ == '__main__':

    # 读取SMI E-FUSE ID
    lines = '0x00_0x12_0xAD_0x10_0x00_0x81_0xD5_0x51'
    Die_info = efuse_to_info(lines)   # Die_infor信息 ['0', '107217472', '5', '34', '185']
    # print(Die_info)

    # 读取Intel Wafer UID

    # line = '2F4A84F0984900F0FF00FF00FF00FF00D0B57B0F67B6FF0F00FF00FF00FF00FF'  # old
    line = '2E653899196105D0FF00FF00FF00FF00D19AC766E69EFA2F00FF00FF00FF00FF'  # new
    lot_number, wafer_number, polarity, x_position, y_position = uid_to_info(line)
    print(lot_number, wafer_number, polarity, x_position, y_position)

    # 从文件中读取，并写入另一个文件
    # read_file = r'C:\Users\yinpeng\Desktop\WorkSpace\Read_UID.txt'
    # file_path = r'C:\Users\yinpeng\Desktop\WorkSpace\Decode_UID.txt'
    # with open(read_file, 'r') as fil:
    #     lines = fil.readlines()
    #     for line in lines:
    #         lot_number, wafer_number, polarity, x_position, y_position = uid_to_info(line.strip()[33:])
    #         with open(file_path, 'a') as file_Open:
    #             file_Open.write("uid: %s " % line.strip()[33:])
    #             file_Open.write("lot_number: %s " % lot_number)
    #             file_Open.write("wafer_number: %s " % wafer_number)
    #             file_Open.write("polarity: %s " % polarity)
    #             file_Open.write("x_position: %s " % x_position)
    #             file_Open.write("y_position: %s\n" % y_position)



