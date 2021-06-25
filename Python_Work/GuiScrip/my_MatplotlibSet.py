# !/usr/bin/python
# -*- coding: utf-8 -*-

class MyLineSet(object):
    def __init__(self):
        self.color = {
            1: 'black',
            2: 'k',
            3: 'dimgray',
            4: 'dimgrey',
            5: 'grey',
            6: 'gray',
            7: 'darkgrey',
            8: 'darkgray',
            9: 'silver',
            10: 'lightgray',
            11: 'lightgrey',
            12: 'gainsboro',
            13: 'whitesmoke',
            14: 'white',
            15: 'w',
            16: 'snow',
            17: 'rosybrown',
            18: 'lightcoral',
            19: 'indianred',
            20: 'brown',
            21: 'firebrick',
            22: 'maroon',
            23: 'darkred',
            24: 'red',
            25: 'r',
            26: 'mistyrose',
            27: 'salmon',
            28: 'tomato',
            29: 'darksalmon',
            30: 'coral',
            31: 'orangered',
            32: 'lightsalmon',
            33: 'sienna',
            34: 'seashell',
            35: 'chocolate',
            36: 'saddlebrown',
            37: 'sandybrown',
            38: 'peachpuff',
            39: 'peru',
            40: 'linen'
            }
        # Marker
        self.marker = {
            1: '.',  # Point
            2: ',',  # Pixel
            3: 'o',  # circle
            4: 'v',  # triangle_down
            5: '^',  # triangle_up
            6: '<',  # triangle_left
            7: '>',  # triangle_right
            8: '1',  # tri-down
            9: '2',  # tri-up
            10: '3',  # tri-left
            11: '4',  # tri-right
            12: '8',  # octagon
            13: 's',  # square
            14: 'p',  # pentagon
            15: 'P',  # plus(filled)
            16: '*',  # star
            17: 'h',  # hexagon1
            18: 'H',  # hexagon2
            19: '+',  # plus
            20: 'x',  # x
            21: 'X',  # X(filled)
            22: 'd',  # diamond
            23: 'D',  # thin_diamond
            24: '|',  # vline
            25: '_',  # hline
            # ==== 高级marker ====
            26: '$ϖ$',  # varpi
            27: '$ϱ$',  # varrho
            28: '$ς$',  # varsigma
            29: '$ϑ$',  # vartheta
            30: '$ξ$',  # xi
            31: '$ζ$',  # zeta
            32: '$Δ$',  # Delta
            33: '$Γ$',  # Gamma
            34: '$Λ$',  # Lambda
            35: '$Ω$',  # Omega
            36: '$Φ$',  # Phi
            38: '$Ψ$',  # Psi
            39: '$Σ$',  # Sigma
            40: '$Θ$',  # Theta
            41: '$Υ$',  # Upsilon
            42: '$Ξ$',  # Xi
            43: '$℧$',  # mho
            44: '$∇$',  # nabla
            45: '$ℵ$',  # aleph
            46: '$ℶ$',  # beth
            47: '$ℸ$',  # daleth
            48: '$ℷ$',  # gimel
            49: '$⇓$',  # Downarrow
            50: '$⇑$',   # Uparrow
            51: '$‖$',   # Vert
            52: '$↓$',   # downarrow
            53: '$⟨$',   # langle
            54: '$⌈$',   # lceil
            55: '$⌊$',   # lfloor
            56: '$⌞$',   # llcorner
            57: '$⌟$',   # lrcorner
            58: '$⟩$',   # rangle
            59: '$⌉$',   # rceil
            60: '$⌋$',   # rfloor
            61: '$⌜$',   # ulcorner
            62: '$↑$',   # uparrow
            63: '$⌝$',   # urcorner
            64: '$⋂$',   # bigcap
            65: '$⋃$',   # bigcup
            66: '$⨀$',   # bigodot
            67: '$⨁$',   # bigoplus
            68: '$⨂$',   # bigotimes
            69: '$⨄$',   # biguplus
            70: '$⋁$',   # bigvee
            71: '$⋀$',   # bigwedge
            72: '$∐$',   # coprod
            73: '$∫$',   # int
            74: '$∮$',  # oint
            75: '$∏$',   # prod
            76: '$∑$'   # sum
            }
        self.linestyle = {
            1: '-',  # solid
            2: '.',  # dotted
            3: '--',  # dashed
            4: '-.',  # dashdot
            }

    def get_color(self, index):
        return self.color[index]

    def get_marker(self, index):
        return self.marker[index]


if __name__ == '__main__':
    color = MyColor().get_color(1)
    print(color)
