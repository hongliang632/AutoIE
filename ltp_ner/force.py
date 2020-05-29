#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re
import datetime

"""
强制合并实体标注。
在LTP之中，先加入的词表，并不会在实体识别中体现。

"""


class force_segmentor(object):

    def __init__(self):
        self.forcelist = []
        self.tagslist = {}

    # 加载词表
    def load(self, filepath):
        with open(filepath, 'r', encoding='utf-8-sig') as file:
            line = file.readline()
            while line:
                if ('#' in line):
                    line = file.readline().strip()
                    continue
                item = force_segmentor_item(line)
                self.forcelist.append(item.get_text())
                self.tagslist[item.get_text()] = item.get_tags()
                line = file.readline()
        try:
            a = self.forcelist[2]
        except:
            print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ':  Error: lexicon is empty')
            exit(0)

        self.compilelist = []
        y = 0
        xlen = 60
        stop = False
        while not stop:
            comstr = '(?:'
            for x in range(xlen):
                z = y * xlen + x
                if z > len(self.forcelist) - 1:
                    stop = True
                    break
                if x > 0:
                    comstr += '|'
                comstr += self.forcelist[z]
            comstr += ')'

            self.compilelist.append(re.compile(comstr))
            y += 1

    def find_in_dict(self, sentence):
        list = []
        de_sentence = sentence
        for compilestr in self.compilelist:
            result = compilestr.findall(de_sentence)

            for x in result:
                list.append(x)

        return list

    def merge(self, sentence, words):
        tag = {}

        indexs_start = []
        index_distance = {}

        found_list = self.find_in_dict(sentence)

        if len(found_list) == 0:
            return words, tag
        for found_word in found_list:

            index_start = -1
            strm = ''
            for i, word in enumerate(words):
                wl = len(word)
                if (index_start == -1 and word == found_word[0:wl]):
                    index_start = i
                    strm += word
                elif (index_start != -1):
                    strm += word
                    if (strm == found_word):
                        if index_start not in indexs_start:
                            indexs_start.append(index_start)

                        index_distance[index_start] = [i - index_start + 1, found_word]
                        index_start = -1
                        strm = ''
                    elif (strm not in found_word):
                        index_start = -1
                        strm = ''

        result = []
        k = 0
        i = 0
        # print indexs_start,index_distance
        while (i < len(words)):
            word = words[i]
            if (i in indexs_start):
                result.append(index_distance[i][1])

                tag[k] = 'S-' + self.tagslist[index_distance[i][1]]
                i += index_distance[i][0]
                k += 1
            else:
                result.append(word)
                i += 1
                k += 1
        return result, tag


class force_segmentor_item(object):

    # 词表形式如下：
    # 天宫一号 spaceship
    # 天宫二号 spaceship
    # Terra对地观测卫星 spaceship
    # TerraSAR-X雷达卫星 spaceship
    def __init__(self, line):
        self.line = line.replace('\r\n', '')
        self.line = self.line.replace('\n', '')

        # 替换括号
        self.line = self.line.replace('(', '（')
        self.line = self.line.replace(')', '）')
        self.text = self.line.split(' ')[0]
        self.tags = self.line.split(' ')[1]
        # self.text = line.replace('\n', '')

    def get_text(self):
        return self.text

    def get_tags(self):
        return self.tags
