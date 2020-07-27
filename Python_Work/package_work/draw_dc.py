import os
import re

def drawdc(filename):
    frnames = []
    with open(filename) as FHIN:
        lines = FHIN.readlines()
        lines = [_.strip('\n') for _ in lines]
        xmclotid, xmcwafer, psmclotid, psmcwafer1, productid = re.split(r'\s+', lines[1].strip())
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

            elif line_key == '110':
                # get the fail region location dimension
                frlx = int(line[4:7])  # frly: Number of FRLs in X-direction for whole chip ->128
                frly = int(line[7:10])   # frly: Number of FRLs in Y-direction for whole chip ->64

            elif line_key == '250':
                dcnames = [tmp.strip() for tmp in re.findall('........', line[6:])]
        chiplines = filter(lambda x: x.startswith('300'), lines)
        chiplines = [line for line in chiplines]
        dclines = filter(lambda x: x.startswith('302'), lines)
        dclines = [line for line in dclines]
        if len(chiplines) == len(dclines):
            for i in range(len(chiplines)):
                x = chiplines[i][3:5]
                y = chiplines[i][5:7]
                print(x, y)

        #
        #     bmpName = frnames[i].replace('/', '').replace('-', '')+'.png'
        #     if os.path.isfile(bmpName):
        #         continue
        #     bmpSize = (cowct * (frlx + 4) + 6, rolct * (frly + 4) + 6)
        #     reticalx = 2
        #     reticaly = 3
        #     newImage = Image.new('RGBA', bmpSize, 'WhiteSmoke')
        #
        #     for chipline, rdline in zip(chiplines, rdlines):
        #         x = int(chipline[3:5])
        #         y = int(chipline[5:7])
        #         create_bmp_from_str(frlx, frly, rdline[3:], "tmp.bmp")
        #         im = Image.open("tmp.bmp")
        #         topLeftX = (x - 1) * (frlx + 4) + 3
        #         topLeftY = bmpSize[1] - y * (frly + 4) - 3
        #         newImage.paste(im, (topLeftX, topLeftY))
        #     for x in range(cowct+1):
        #         if x % reticalx == 1:   # 调整X方向的Retical
        #             newImage.paste("red", (x * (frlx + 4), 0, x * (frlx + 4) + 2, bmpSize[1]))
        #     for y in range(rolct + 1):
        #         if y % reticaly == 0:
        #             newImage.paste("red", (0, y * (frly + 4), bmpSize[0], y * (frly + 4) + 2))
        #     if fnloc == 0:
        #         newImage = newImage.rotate(180)
        #     newImage.save(bmpName, 'PNG')


if __name__ == '__main__':
    path = r'C:\Users\yinpeng\Desktop\PPB020\CP_P_PPB020.106_08_1'
    drawdc(path)
