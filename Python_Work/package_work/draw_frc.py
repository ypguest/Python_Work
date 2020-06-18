import os
import struct
import re
from PIL import Image


def create_bmp_from_str(w, h, tarstr, bmpName):
    fileData = open(bmpName, 'wb')
    fileData.write(struct.pack('B', 0x42))
    fileData.write(struct.pack('B', 0x4d))
    fileData.write(
        struct.pack('L', 0x3e + int(w * h / 8)))    # this is the only part need to change due to the size of the RD file  4096/8192
    # 3e bmp
    fileData.write(struct.pack('H', 0x0000))
    fileData.write(struct.pack('H', 0x0000))
    fileData.write(struct.pack('L', 0x0000003e))
    fileData.write(struct.pack('L', 0x00000028))  # the size of the head
    fileData.write(struct.pack('L', w))  # the width of bmp file this time is 128
    fileData.write(struct.pack('L', h))  # the height of the bmp file this time is 64
    fileData.write(struct.pack('H', 0x0001))  # always 1
    fileData.write(struct.pack('H', 0x0001))  # the bit number of one pix
    fileData.write(struct.pack('L', 0x00000000))  # the compress mode
    fileData.write(struct.pack('L', w * h))  # the size of the bmp file by BYTE
    fileData.write(struct.pack('L', 0x00000000))  # always 0
    fileData.write(struct.pack('L', 0x00000000))  # always 0
    fileData.write(struct.pack('L', 0x00000000))  # always 0
    fileData.write(struct.pack('L', 0x00000000))  # always 0
    fileData.write(struct.pack('L', 0x00000000))  # always 0
    fileData.write(struct.pack('L', 0x00ffffff))  # always 0
    tmpList = re.findall('........', tarstr)
    for fourBit in tmpList:
        if fourBit.startswith(' '):
            fileData.write(struct.pack('>L', 0xffffffff))  # always 0
        else:
            fileData.write(struct.pack('>L', 0xffffffff - int('0x' + fourBit, 16)))  # always 0
    fileData.close()


def createrdmap(filename):
    frnames = []
    frlx = 0
    frly = 0
    with open(filename) as FHIN:
        lines = FHIN.readlines()
        lines = [_.strip('\n') for _ in lines]
        # lotid, wafer, lotid1, wafer1, lot2 = re.split(r'\s+', lines[1].strip())
        # print(lotid, wafer, lotid1, wafer1, lot2 )
        for line in lines[9:]:
            if line == '':
                break
            line = line.strip('\n')
            if line.startswith(' '):
                continue
            line_key = line[:3]

            if line_key == '107':
                fnloc = int(line[3:6])  # Notch location 000: down, 090: left, 180: up, 270: right
                # orloc = int(line[6:7])  # XY origin:   1: upper right; 2: upper left; 3: lower left; 4: lower right
                cowct = int(line[7:9])  # Number of columns (X)
                rolct = int(line[9:11])  # Number of rows (Y)
                # print(cowct,rolct)

            elif line_key == '110':
                # get the fail region location dimension
                frlx = int(line[4:7])  # frly: Number of FRLs in X-direction for whole chip ->128
                frly = int(line[7:10])   # frly: Number of FRLs in Y-direction for whole chip ->64

            elif line_key == '200':
                frnames = [tmp.strip() for tmp in re.findall('.......', line[8:]) if tmp[:4] == 'R/D-']

        chiplines = filter(lambda x: x.startswith('300'), lines)
        chiplines = [line for line in chiplines]
        for i in range(len(frnames)):
            rdlines = filter(lambda x: x.startswith(str(int(450+i*10))), lines)
            rdlines = [line for line in rdlines]
            bmpName = frnames[i].replace('/', '').replace('-', '')+'.png'
            if os.path.isfile(bmpName):
                continue
            bmpSize = (cowct * (frlx + 4) + 6, rolct * (frly + 4) + 6)
            reticalx = 2
            reticaly = 3
            newImage = Image.new('RGBA', bmpSize, 'WhiteSmoke')

            for chipline, rdline in zip(chiplines, rdlines):
                x = int(chipline[3:5])
                y = int(chipline[5:7])
                create_bmp_from_str(frlx, frly, rdline[3:], "tmp.bmp")
                im = Image.open("tmp.bmp")
                topLeftX = (x - 1) * (frlx + 4) + 3
                topLeftY = bmpSize[1] - y * (frly + 4) - 3
                newImage.paste(im, (topLeftX, topLeftY))
            for x in range(cowct+1):
                if x % reticalx == 1:   # 调整X方向的Retical
                    newImage.paste("red", (x * (frlx + 4), 0, x * (frlx + 4) + 2, bmpSize[1]))
            for y in range(rolct + 1):
                if y % reticaly == 0:
                    newImage.paste("red", (0, y * (frly + 4), bmpSize[0], y * (frly + 4) + 2))
            if fnloc == 0:
                newImage = newImage.rotate(180)
            newImage.save(bmpName, 'PNG')


if __name__ == '__main__':
    path = r'C:\Users\yinpeng\Desktop\WorkSpace\CP_P_BJN865000_01_1'
    createrdmap(path)
