#!/usr/bin/env python
# -*- coding:utf-8 -*-
import pyltp
import os
import re
import datetime
import warnings
from warnings import simplefilter
from ltp_ner.force import force_segmentor
from ltp_ner.hlog import hlogger
from typing import List, Any, Dict

""" 
加载数据
自然语言处理
提取实体
"""

__all__ = ['sentence',
           'entity']

simplefilter(action='ignore', category=FutureWarning)
warnings.filterwarnings("ignore")

Path = str


# 处理entence
def sentence(articles: List[Dict], project: Path = os.getcwd(),
             ltp_dir=os.path.abspath(os.path.join(os.path.realpath(__file__), "../..")) + '/ltp_data') -> List[Dict]:
    logger = hlogger(project)
    start_time = datetime.datetime.now()
    logger.info('Starting to process sentences')

    # 加载ltp相关模型
    # 分词模型
    segmentor = pyltp.Segmentor()
    segmentor.load(os.path.join(ltp_dir, "cws.model"))

    # 词性模型
    postagger = pyltp.Postagger()
    postagger.load(os.path.join(ltp_dir, 'pos.model'))

    # 命名实体模型
    recognizer = pyltp.NamedEntityRecognizer()
    recognizer.load(os.path.join(ltp_dir, 'ner.model'))

    if_force = False
    # 如果存在词表，强制实体标注加载词表
    if os.path.exists(project + '/lexicon'):
        logger.info('Ner will use lexicon')
        if_force = force_segmentor()
        if_force.load(project + '/lexicon')

    logger.info('Processing sentences')

    results = []
    for article in articles:
        result = extract_information(article['id'], article['content'], segmentor, postagger, recognizer,
                                     if_force)
        results.extend(result)

    length = len(results)

    end_time = datetime.datetime.now()

    logger.info('Sentences have been processed successfully,and there are %s sentences' % len(results))
    logger.info('FINISHED! using time : %s\n' % get_time((end_time - start_time).seconds))

    return results


# 生成实体entity

def entity(sentences: List[Dict], tag: List, project: Path = os.getcwd()) -> List[Dict]:
    logger = hlogger(project)
    start_time = datetime.datetime.now()

    logger.info('Starting to extract entity_mention')
    logger.info('Extracting entity_mention')

    results = {}
    length = 0
    for row in sentences:
        # sentence_id, sentence_text, ner_tags
        result, num = extract_entity(row['tokens'], row['ner_tags'], tag=tag)
        row.update(result)
        length += num

    end_time = datetime.datetime.now()
    logger.info('Entities have been extracted successfully, and there are %s  entities' % length)
    logger.info('FINISHED! using time : %s\n' % get_time((end_time - start_time).seconds))

    return sentences


# 自然语言处理
def extract_information(doc_id, content, segmentor, postagger, recognizer, force_segmentor) -> List[Dict]:
    # 提取文本信息
    # 分句
    sents = pyltp.SentenceSplitter.split(content)

    for index, sent in enumerate(list(sents)):

        doc_id = doc_id
        sentence_index = index + 1
        sentence_text = sent
        tokens = list(segmentor.segment(sent))
        words = list(tokens)
        if force_segmentor:
            a = force_segmentor.merge(sent, words)
            words = a[0]
            tag = a[1]

        # pos_tags:词性
        pos_tags = list(postagger.postag(words))

        # ner_tags:命名实体
        ner_tags = list(recognizer.recognize(words, pos_tags))
        if force_segmentor:
            for t in tag.keys():
                ner_tags[t] = tag[t]

        yield {'sentence_id': '%s_%d' % (doc_id, sentence_index), 'sentence_text': sentence_text, 'tokens': words,
               'ner_tags': ner_tags}


# 提取特定类型的实体
def extract_entity(tokens, ner_tags, tag) -> List[Dict]:
    # 提取我们需要的实体类型
    # t为实体类型
    mention = {}
    num = 0
    for t in tag:
        mention[tag[t]] = []
        num_tokens = len(ner_tags)

        # 找到第一个被标注的词
        first_indexes = (i for i in range(num_tokens) if
                         t in ner_tags[i] and (i == 0 or t not in ner_tags[i - 1]) and re.match(
                             u'^[\u4e00-\u9fa5\u3040-\u309f\u30a0-\u30ffa-zA-Z]+$', str(tokens[i])) != None)
        for begin_index in first_indexes:
            # 找到后续被标注的词
            end_index = begin_index + 1
            while end_index < num_tokens and t in ner_tags[end_index] and re.match(
                    u'^[\u4e00-\u9fa5\u3040-\u309f\u30a0-\u30ffa-zA-Z]+$', str(tokens[end_index])) != None:
                end_index += 1
            end_index -= 1

            mention_text = "".join(map(lambda i: tokens[i], range(begin_index, end_index + 1)))
            temp_text = mention_text

            # 判断实体是否过长以及去掉不符合要求的实体
            if temp_text == None or temp_text == '':
                continue
            # if end_index - begin_index >= 25:
            #   continue
            mention[tag[t]].append(mention_text)
            num += 1
    return mention, num


def get_time(all_seconds: str) -> str:
    days, temp = divmod(all_seconds, 86400)
    hours, temp = divmod(temp, 3600)
    minute, temp = divmod(temp, 60)
    seconds = temp
    timestr = str(seconds) + ' seconds '
    if minute != 0:
        timestr = str(minute) + ' minutes ' + timestr
    if hours != 0:
        timestr = str(hours) + ' hours ' + timestr
    if days != 0:
        timestr = str(days) + ' days ' + timestr
    return timestr
