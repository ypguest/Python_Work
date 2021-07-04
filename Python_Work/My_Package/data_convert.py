#!/usr/bin/python
#-*- coding: utf-8 -*-

import re

base = [str(x) for x in range(10)] + [chr(x) for x in range(ord('A'), ord('A') + 6)]

def bin2dec(string_num): #二进制 to 十进制
    return str(int(string_num, 2))

def hex2dec(string_num):    #十六进制 to 十进制
    return str(int(string_num.upper(), 16))

def dec2bin(string_num):    #十进制 to 二进制
    num = int(string_num)
    mid = []
    while True:
        if num == 0: break
        num, rem = divmod(num, 2)
        mid.append(base[rem])
    return ''.join([str(x) for x in mid[::-1]])
def dec2hex(string_num):    #十进制 to 十六进制
    num = int(string_num)
    mid = []
    while True:
        if num == 0: break
        num, rem = divmod(num, 16)
        mid.append(base[rem])

    return ''.join([str(x) for x in mid[::-1]])
def hex2bin(string_num):    #十六进制 to 二进制
    data_lens = -len(string_num) * 4
    data_len = len(string_num) * 4
    data ='0'*data_len+str(dec2bin(hex2dec(string_num.upper())))
    return data[data_lens:]

def bin2hex(string_num):    #二进制 to 十六进制
    return dec2hex(bin2dec(string_num))


def lot_cov(lot_id):
    textArr = ''
    textArr = re.findall('.{' + str(6) + '}', lot_id)
    comp = {
     '000000': '0',
     '000001': '1',
     '000010': '2',
     '000011': '3',
     '000100': '4',
     '000101': '5',
     '000110': '6',
     '000111': '7',
     '001000': '8',
     '001001': '9',
     '001010': 'A',
     '001011': 'B',
     '001100': 'C',
     '001101': 'D',
     '001110': 'E',
     '001111': 'F',
     '010000': 'G',
     '010001': 'H',
     '010010': 'I',
     '010011': 'J',
     '010100': 'K',
     '010101': 'L',
     '010110': 'M',
     '010111': 'N',
     '011000': 'O',
     '011001': 'P',
     '011010': 'Q',
     '011011': 'R',
     '011100': 'S',
     '011101': 'T',
     '011110': 'U',
     '011111': 'V',
     '100000': 'W',
     '100001': 'X',
     '100010': 'Y',
     '100011': 'Z',
    }
    lot_id_cov = comp[textArr[0]] + comp[textArr[1]] + comp[textArr[2]] + comp[textArr[3]] + comp[textArr[4]]
    return lot_id_cov
