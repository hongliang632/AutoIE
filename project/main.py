#!/usr/bin/env python
# -*- coding:utf-8 -*-
from ltp_ner.hio import *
from ltp_ner.extraction import *

if __name__ == "__main__":
    TAG = {'Nh': '人名', 'Ns': '地名', 'Ni': '机构名'}
    LTP = '/home/nuc/桌面/gBuilder3/ltp_data'
    articles = load_csv('articles.csv')
    sentences = sentence(articles=articles[0:100], ltp_dir=LTP)
    entity(sentences=sentences, tag=TAG)
    save_csv(filepath='entity.csv',data=sentences)

