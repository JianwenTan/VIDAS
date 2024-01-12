# -*- coding: UTF-8 -*-
class Data_matrix:

    def __init__(self):
        self.mixture_A = [['', '', '', '', ''],
                          ['榆树    ', '', '猫上皮  ', '', '葎草    '],
                          ['', '花生    ', '', '蟹      ', ''],
                          ['鸡蛋    ', '', '开/榛   ', '', '西红柿  '],
                          ['', '悬铃木  ', '', '大豆    ', ''],
                          ['小麦    ', '', '普通豚草', '', '鳕鱼    '],
                          ['', '点/烟/交', '', '狗上皮  ', ''],
                          ['蟑螂    ', '', '虾      ', '', '牛奶    '],
                          ['', '屋/粉   ', '', '艾蒿    ', '']]

        self.mixture_B = [['', '', '', '', ''],
                          ['黄/果/黑', '', '猫上皮  ', '', '苦艾    '],
                          ['', '花生    ', '', '分/毛/根', ''],
                          ['蛋清    ', '', '棉絮    ', '', '烟草屑  '],
                          ['', '杨/柳   ', '', '大豆    ', ''],
                          ['蜜蜂毒  ', '', '普通豚草', '', '蒲公英  '],
                          ['', '交链孢霉', '', '狗上皮  ', ''],
                          ['柏树    ', '', '蚊子唾液', '', '牛奶    '],
                          ['', '屋尘螨  ', '', '艾蒿    ', '']]

        self.mixture_C = [['', '', '', '', ''],
                          ['点/分/烟', '', '猫上皮  ', '', '葎草    '],
                          ['', '花生    ', '', '蟹      ', ''],
                          ['鸡蛋    ', '', '普通豚草', '', '鳕/龙/扇'],
                          ['', '柳/杨/榆', '', '大豆    ', ''],
                          ['羊肉    ', '', '虾      ', '', '屋尘    '],
                          ['', '牛肉    ', '', '狗上皮  ', ''],
                          ['蟑螂    ', '', 'CCD     ', '', '牛奶    '],
                          ['', '屋/粉   ', '', '艾蒿    ', '']]

        self.mixture_D = [['', '', '', '', ''],
                          ['', '鳕/鲑/鲈', '', '', ''],
                          ['点/烟/分', '', '猫/狗   ', '', '总IgE   '],
                          ['', '柏/榆/悬', '', '', ''],
                          ['鸡蛋    ', '', '普/艾/苦', '', ''],
                          ['', '牛/羊   ', '', '虾/蟹/扇', ''],
                          ['花/开/腰', '', '屋尘    ', '', ''],
                          ['', '屋/粉   ', '', '芒/菠/苹', ''],
                          ['', '', '牛奶    ', '', '']]

        self.result = [
            ' - ', ' + ', '++ ', '+++'
        ]
